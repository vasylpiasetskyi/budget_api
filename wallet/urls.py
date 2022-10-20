from django.urls import path

from wallet.views import AccountAPIList, AccountAPIDetail, CategoryAPIList, CategoryAPIDetail, SubCategoryAPIList, \
    SubCategoryAPIDetail

urlpatterns = [
    path('account/', AccountAPIList.as_view()),
    path('account/<int:pk>/', AccountAPIDetail.as_view()),
    path('category/', CategoryAPIList.as_view()),
    path('category/<int:pk>/', CategoryAPIDetail.as_view()),
    path('category/<int:pk>/subcategory/', SubCategoryAPIList.as_view()),
    path('category/<int:pk>/subcategory/<int:sub_pk>/', SubCategoryAPIDetail.as_view()),

]
