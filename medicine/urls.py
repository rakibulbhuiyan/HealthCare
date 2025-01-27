from django.urls import path
from .views import (CategoryListView, SubCategoryListView, MedicineListView, MedicneSearchView,
             CartView, InitializePaymentView, CompletePaymentView, VerifyPaymentView,
             Bkash_ExecutePaymentView,Bkash_InitializePaymentView,Bkash_VerifyPaymentView,
              DietCategoryView,DietPlanView)
from .check_out import AddressView, CheckoutView

urlpatterns = [
    # Category
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category-detail'),

    # Subcategory
    path('categories/<int:category_id>/subcategories/', SubCategoryListView.as_view(), name='subcategory-list'),
    path('categories/<int:category_id>/subcategories/<int:pk>/', SubCategoryListView.as_view(), name='subcategory-detail'),
    
    # Medicine
    path('subcategories/<int:sub_category_id>/medicines/', MedicineListView.as_view(), name='medicine-list'),
    path('subcategories/<int:sub_category_id>/medicines/<int:pk>/', MedicineListView.as_view(), name='medicine-detail'),
    path('medicines/search/', MedicneSearchView.as_view(), name='medicine-search'),
    
    # CartItem  
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart-item-detail'),

    #  Checkout System
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('address/', AddressView.as_view(), name='address'),

    # Nagad payment URL
    path('payment/initialize/', InitializePaymentView.as_view(), name='initialize_payment'),
    path('payment/complete/<str:payment_reference_id>/', CompletePaymentView.as_view(), name='complete_payment'),
    path('payment/verify/<str:payment_reference_id>/', VerifyPaymentView.as_view(), name='verify_payment'),
    
    # Bkash Payment URL
    path('bkash/initiate/', Bkash_InitializePaymentView.as_view(), name='bkash-initiate'),
    path('bkash/execute/<str:payment_id>/', Bkash_ExecutePaymentView.as_view(), name='bkash-execute'),
    path('bkash/verify/<str:payment_id>/', Bkash_VerifyPaymentView.as_view(), name='bkash-verify'),

    # Diet plan URL
    path('diet_categories/', DietCategoryView.as_view(), name='diet_categories'),
    path('diet_category_detail/<int:pk>/', DietCategoryView.as_view(), name='diet_category_detail'),
    path('diet_plans/', DietPlanView.as_view(), name='diet_plans'),
    path('diet_plan_detail/<int:pk>/', DietPlanView.as_view(), name='diet_plan_detail'),
]
