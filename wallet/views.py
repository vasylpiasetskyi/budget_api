import decimal

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

    # def get_serializer_class(self):
    #     if "transfer" in str(self.request):
    #         return TransactionCreateTransferSerializer
    #     return TransactionCreateSerializer

    def perform_create(self, serializer):
        from_account = None
        to_account = None
        owner = self.request.user
        category = serializer.validated_data.get('category')
        sub_category = serializer.validated_data.get('sub_category')

        if category and category.owner != owner:
            raise NotFound(detail=f"Error 403, Category does not meet the {owner.username}", code=403)

        if serializer.validated_data.get('from_account'):
            from_account = Account.objects.get(id=serializer.validated_data.get('from_account').id)
            if from_account.owner != owner:
                raise NotFound(detail=f"Error 403, Account does not meet the {owner.username}", code=403)

        if serializer.validated_data.get('to_account'):
            to_account = Account.objects.get(id=serializer.validated_data.get('to_account').id)
            if to_account.owner != owner:
                raise NotFound(detail=f"Error 403, Account does not meet the {owner.username}", code=403)

        if serializer.validated_data.get('action') == "INCOME":
            if category and category.category_type != "INCOME":
                raise NotFound(detail=f"Error 403, Category does not meet the INCOME", code=403)
            if sub_category and sub_category.category.category_type != "INCOME":
                raise NotFound(detail=f"Error 403, SubCategory does not meet the INCOME", code=403)
            to_account.balance = to_account.balance + decimal.Decimal(serializer.validated_data.get('amount'))
            to_account.save()
            serializer.save(from_account=None)

        if serializer.validated_data.get('action') == "EXPENSE":
            if category and category.category_type != "EXPENSE":
                raise NotFound(detail=f"Error 403, Category does not meet the EXPENSE", code=403)
            if sub_category and sub_category.category.category_type != "EXPENSE":
                raise NotFound(detail=f"Error 403, SubCategory does not meet the EXPENSE", code=403)
            from_account.balance = from_account.balance - decimal.Decimal(serializer.validated_data.get('amount'))
            from_account.save()
            serializer.save(to_account=None)

        if serializer.validated_data.get('action') == "TRANSFER":
            if not from_account or not to_account:
                raise NotFound(detail=f"Error 403, Transfer required FROM and TO accounts", code=403)
            if category or sub_category:
                raise NotFound(detail=f"Error 403, Transfer does not have Category or SubCategory", code=403)
            to_account.balance = to_account.balance + decimal.Decimal(serializer.validated_data.get('amount'))
            from_account.balance = from_account.balance - decimal.Decimal(serializer.validated_data.get('amount'))
            to_account.save()
            serializer.save(category=None, sub_category=None)

        return serializer


class SubCategoryAPIDetailStaff(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH, DELETE, HEAD, OPTIONS"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionUpdateSerializer




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
