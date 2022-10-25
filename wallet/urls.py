from django.urls import path

from wallet import views

urlpatterns = [


    # Account
    path('account/', views.AccountAPIList.as_view()),
    path('account/create/', views.AccountAPICreate.as_view()),
    path('account/<int:pk>/', views.AccountAPIDetail.as_view()),

    # Category
    path('category/', views.CategoryAPIList.as_view()),
    path('category/create/', views.CategoryAPICreate.as_view()),
    path('category/<int:pk>/', views.CategoryAPIDetail.as_view()),

    # Sub_category
    path('subcategory/', views.SubCategoryAPIList.as_view()),
    path('subcategory/create/', views.SubCategoryAPICreateStaff.as_view()),
    path('subcategory/<int:pk>/', views.SubCategoryAPIDetailStaff.as_view()),
    # Sub_category - old
    path('category/<int:pk>/subcategory/', views.SubCategoryAPIList.as_view()),
    path('category/<int:pk>/subcategory/create/', views.SubCategoryAPICreate.as_view()),
    path('category/<int:pk>/subcategory/<int:sub_pk>/', views.SubCategoryAPIDetail.as_view()),

    # Transaction
    path('transaction/', views.TransactionAPIList.as_view()),
    path('transaction/create/', views.TransactionAPICreate.as_view()),
    path('transaction/<int:pk>/', views.SubCategoryAPIDetailStaff.as_view()),

]
