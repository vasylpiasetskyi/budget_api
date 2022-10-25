from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from wallet.models import Currency, Account, Category, SubCategory, Transaction


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


# CURRENCY ###
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "name", "code", "exchange")


# ACCOUNT ###
class AccountListSerializer(serializers.ModelSerializer):
    owner = CurrentUserSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Account
        fields = ("id", "account_type", "name", "balance", "owner", "currency")


class AccountCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = ("account_type", "name", "balance", "owner", "currency")

    def create(self, validated_data):
        account, _ = Account.objects.update_or_create(
            account_type=validated_data.get('account_type', "Regular"),
            name=validated_data.get('name', "Money"),
            balance=validated_data.get('balance', 0),
            owner=validated_data.get('owner', None),
            # owner=self.context['request'].user,
            currency=validated_data.get('currency', 0),
        )
        return account


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


# SUBCATEGORY ###
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", "name", "category", "created_at", "updated_at", "is_active")


class SubCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("name",)


class SubCategoryCreateSerializerStaff(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", "name", "category")


class SubCategoryUpdateSerializer(SubCategoryCreateSerializer):
    pass


# CATEGORY ###
class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True)
    owner = CurrentUserSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Category
        fields = (
            "id", "name", "sub_category", "owner", "category_type", "currency", "is_active", "created_at", "updated_at"
        )


class CategorySerializerForAccount(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = Category
        fields = (
            "id", "name", "category_type", "currency", "is_active")


class CategoryCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ("name", "category_type", "currency")

    def create(self, validated_data):
        category, _ = Category.objects.update_or_create(
            name=validated_data.get('name', "Category"),
            owner=validated_data.get('owner', None),
            # owner=self.context['request'].user,
            category_type=validated_data.get('category_type', "None"),
            currency=validated_data.get('currency', None),
        )
        return category


# TRANSACTION ###
class TransactionSerializer(serializers.ModelSerializer):
    owner = CurrentUserSerializer()
    category = CategorySerializerForAccount()
    sub_category = SubCategorySerializer()
    from_account = AccountDetailSerializer()
    to_account = AccountDetailSerializer()

    class Meta:
        model = Transaction
        fields = "__all__"


class TransactionCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        exclude = ("created_at", "updated_at",)

    def create(self, validated_data):
        transaction, _ = Transaction.objects.update_or_create(
            action=validated_data.get('action', "EXPENSE"),
            owner=validated_data.get('owner', None),
            # owner=self.context['request'].user,
            category=validated_data.get('category', "None"),
            sub_category=validated_data.get('sub_category', "None"),
            from_amount=validated_data.get('from_amount', 0),
            to_amount=validated_data.get('to_amount', 0),
            description=validated_data.get('description', "None"),
            date=validated_data.get('date', datetime.now()),
            from_account=validated_data.get('from_account', "None"),
            to_account=validated_data.get('to_account', "None"),
        )
        return transaction


class TransactionUpdateSerializer(TransactionCreateSerializer):
    pass
