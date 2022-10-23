from datetime import datetime

from rest_framework import serializers

from wallet.models import Currency, Account, Category, SubCategory, Transaction


# CURRENCY ###
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("name", "code", "exchange")


# ACCOUNT ###
class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("account_type", "name", "balance", "owner", "currency")


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("__all__")


# CATEGORY ###
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("__all__")


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "category_type", "currency")

    def create(self, validated_data):
        category, _ = Category.objects.update_or_create(
            name=validated_data.get('name', "Category"),
            owner=self.context['request'].user,
            category_type=validated_data.get('category_type', "None"),
            currency=validated_data.get('currency', None),
        )
        return category


# SUBCATEGORY ###
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", "name", "category", "created_at", "updated_at", "is_active")


class SubCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("name",)


class SubCategoryUpdateSerializer(SubCategoryCreateSerializer):
    pass


# TRANSACTION ###
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("__all__")


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ("created_at", "updated_at", "owner")

    def create(self, validated_data):
        transaction, _ = Transaction.objects.update_or_create(
            action=validated_data.get('action', "EXPENSE"),
            owner=self.context['request'].user,
            category=validated_data.get('category', "None"),
            sub_category=validated_data.get('sub_category', "None"),
            amount=validated_data.get('amount', 0),
            description=validated_data.get('description', "None"),
            date=validated_data.get('date', datetime.now()),
            from_account=validated_data.get('from_account', "None"),
            to_account=validated_data.get('to_account', "None"),
        )
        return transaction


class TransactionCreateTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ("created_at", "updated_at", "action", "owner", "category", "sub_category")

    def create(self, validated_data):
        transaction, _ = Transaction.objects.update_or_create(
            action="TRANSFER",
            owner=self.context['request'].user,
            category=None,
            sub_category=None,
            amount=validated_data.get('amount', 0),
            description=validated_data.get('description', "None"),
            date=validated_data.get('date', datetime.now()),
            from_account=validated_data.get('from_account', "None"),
            to_account=validated_data.get('to_account', "None"),
        )
        return transaction
