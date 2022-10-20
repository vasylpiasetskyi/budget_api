from rest_framework import generics

from wallet.models import Account, Category, SubCategory
from wallet.serializers import (AccountListSerializer, AccountDetailSerializer, CategorySerializer,
                                SubCategorySerializer)


class AccountAPIList(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer

    def get_queryset(self):
        return Account.objects.all().filter(owner=self.request.user)


class AccountAPIDetail(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer


class CategoryAPIList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all().filter(owner=self.request.user)


class CategoryAPIDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryAPIList(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        return SubCategory.objects.all().filter(category=pk)


class SubCategoryAPIDetail(generics.RetrieveAPIView):
    serializer_class = SubCategorySerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'sub_pk'

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        sub_pk = self.kwargs.get('sub_pk', None)
        return SubCategory.objects.all().filter(category=pk, id=sub_pk)
