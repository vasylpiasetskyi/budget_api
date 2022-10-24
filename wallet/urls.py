from django.urls import path

from wallet import views

urlpatterns = [
    path('account/', views.AccountAPIList.as_view()),
    path('account/<int:pk>/', views.AccountAPIDetail.as_view()),

    path('category/', views.CategoryAPIList.as_view()),
    path('category/create/', views.CategoryAPICreate.as_view()),

    path('category/<int:pk>/', views.CategoryAPIDetail.as_view()),
    path('category/<int:pk>/subcategory/', views.SubCategoryAPIList.as_view()),
    path('category/<int:pk>/subcategory/create/', views.SubCategoryAPICreate.as_view()),
    path('category/<int:pk>/subcategory/<int:sub_pk>/', views.SubCategoryAPIDetail.as_view()),

    path('subcategory/', views.SubCategoryAPIList.as_view()),
    path('subcategory/create/', views.SubCategoryAPICreateStaff.as_view()),
    path('subcategory/<int:pk>/', views.SubCategoryAPIDetailStaff.as_view()),

    path('transaction/', views.TransactionAPIList.as_view()),
    path('transaction/create/', views.TransactionAPICreate.as_view()),
    path('transaction/<int:pk>/', views.SubCategoryAPIDetailStaff.as_view()),

]
