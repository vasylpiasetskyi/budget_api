import decimal

from rest_framework import generics

from wallet.models import Account, Category, SubCategory, Transaction
from wallet.serializers import (AccountListSerializer, AccountDetailSerializer, CategorySerializer,
                                SubCategorySerializer, CategoryCreateSerializer, SubCategoryCreateSerializer,
                                SubCategoryUpdateSerializer, TransactionSerializer, TransactionCreateSerializer,
                                TransactionCreateTransferSerializer,

                                )


# ACCOUNT VIEW ###
class AccountAPIList(generics.ListAPIView):
    """GET, HEAD, OPTIONS"""
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer

    def get_queryset(self):
        return Account.objects.all().filter(owner=self.request.user)


class AccountAPIDetail(generics.RetrieveAPIView):
    """GET, HEAD, OPTIONS"""
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer


# CATEGORY VIEW ###
class CategoryAPIList(generics.ListAPIView):
    """GET, HEAD, OPTIONS"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all().filter(owner=self.request.user)


class CategoryAPICreate(generics.CreateAPIView):
    """POST, OPTIONS"""
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class CategoryAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE, HEAD, OPTION"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# SUBCATEGORY VIEW ###
class SubCategoryAPIList(generics.ListAPIView):
    """GET, HEAD, OPTIONS"""
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        return SubCategory.objects.all().filter(category=pk)


class SubCategoryAPICreate(generics.CreateAPIView):
    """POST, OPTIONS"""
    lookup_field = 'pk'
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryCreateSerializer

    def perform_create(self, serializer):
        category = Category.objects.get(id=self.kwargs.get('pk', None))
        return serializer.save(category=category, )


class SubCategoryAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE, HEAD, OPTIONS"""
    serializer_class = SubCategoryUpdateSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'sub_pk'

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        sub_pk = self.kwargs.get('sub_pk', None)
        return SubCategory.objects.all().filter(category=pk, id=sub_pk)


# TRANSACTION VIEW ###
class TransactionAPIList(generics.ListAPIView):
    """GET, HEAD, OPTIONS"""
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all().filter(owner=self.request.user)


class TransactionAPICreate(generics.CreateAPIView):
    """POST, OPTIONS"""

    queryset = Transaction.objects.all()

    def get_serializer_class(self):
        if "transfer" in str(self.request):
            return TransactionCreateTransferSerializer
        return TransactionCreateSerializer

    # serializer_class = TransactionCreateSerializer
    # serializer_class = TransactionCreateTransferSerializer

    def perform_create(self, serializer):
        from_account = Account.objects.get(id=serializer.validated_data['from_account'].id)
        from_account.balance = from_account.balance - decimal.Decimal(serializer.validated_data['amount'])
        from_account.save()
        if "transfer" in str(self.request):
            to_account = Account.objects.get(id=serializer.validated_data['to_account'].id)
            to_account.balance = to_account.balance + decimal.Decimal(serializer.validated_data['amount'])
            to_account.save()
        return serializer.save()

#
#
# class SubCategoryAPIDetail(generics.RetrieveUpdateDestroyAPIView):
#     """GET, PUT, PATCH, DELETE, HEAD, OPTIONS"""
#     serializer_class = SubCategoryUpdateSerializer
#     lookup_field = 'pk'
#     lookup_url_kwarg = 'sub_pk'
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk', None)
#         sub_pk = self.kwargs.get('sub_pk', None)
#         return SubCategory.objects.all().filter(category=pk, id=sub_pk)
