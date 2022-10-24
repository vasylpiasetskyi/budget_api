import decimal

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from wallet.models import Account, Category, SubCategory, Transaction
from wallet.serializers import (AccountListSerializer, AccountDetailSerializer, CategorySerializer,
                                SubCategorySerializer, CategoryCreateSerializer, SubCategoryCreateSerializer,
                                SubCategoryUpdateSerializer, TransactionSerializer, TransactionCreateSerializer,
                                SubCategoryCreateSerializerStaff,
                                TransactionUpdateSerializer,
                                )

from wallet.services import service_perform_create, update_accounts_balance


# ACCOUNT VIEW ###
class AccountAPIList(generics.ListAPIView):
    """GET, HEAD, OPTIONS"""
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer

    def get_queryset(self):
        return Account.objects.all().filter(owner=self.request.user)


class AccountAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE, HEAD, OPTION"""
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        transactions = Transaction.objects.filter(Q(from_account=instance.id) | Q(to_account=instance.id))
        for transaction in transactions:
            transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        transactions = Transaction.objects.filter(category=instance.id)
        for transaction in transactions:
            update_accounts_balance(transaction)
            transaction.delete()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# SUBCATEGORY VIEW ###
class SubCategoryAPIList(generics.ListAPIView):
    """GET, HEAD, OPTIONS"""
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        if pk:
            return SubCategory.objects.all().filter(category=pk)
        return SubCategory.objects.all().filter()


class SubCategoryAPICreate(generics.CreateAPIView):
    """POST, OPTIONS"""
    lookup_field = 'pk'
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryCreateSerializer

    def perform_create(self, serializer):
        category = Category.objects.get(id=self.kwargs.get('pk', None))
        return serializer.save(category=category, )


class SubCategoryAPICreateStaff(generics.CreateAPIView):
    """POST, OPTIONS"""
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryCreateSerializerStaff


class SubCategoryAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE, HEAD, OPTIONS"""
    serializer_class = SubCategoryUpdateSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'sub_pk'

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        sub_pk = self.kwargs.get('sub_pk', None)
        if sub_pk:
            return SubCategory.objects.all().filter(category=pk, id=sub_pk)
        return SubCategory.objects.all()


class SubCategoryAPIDetailStaff(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE, HEAD, OPTIONS"""
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryUpdateSerializer


# TRANSACTION VIEW ###
class TransactionAPIList(generics.ListAPIView):
    """GET, HEAD, OPTIONS"""
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all().filter(owner=self.request.user)


class TransactionAPICreate(generics.CreateAPIView):
    """POST, OPTIONS"""
    serializer_class = TransactionCreateSerializer
    queryset = Transaction.objects.all()

    def perform_create(self, serializer):
        return service_perform_create(self, serializer)


class SubCategoryAPIDetailStaff(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE, HEAD, OPTIONS"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionUpdateSerializer

    def perform_update(self, serializer):
        return service_perform_create(self, serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        update_accounts_balance(instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
