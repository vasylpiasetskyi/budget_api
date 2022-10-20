from rest_framework import serializers

from wallet.models import Currency, Account, Category, SubCategory, Transaction


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("name", "code", "exchange")


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("account_type", "name", "balance", "owner", "currency")


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("__all__")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("__all__")


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", "name", "category","created_at", "updated_at", "is_active")


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("__all__")
