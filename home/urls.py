from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import global_settings
from home import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add_sales/', views.AddSalesView.as_view(), name='add_sales'),
    path('approve_sale/<sale_id>/',views.ApproveSaleView.as_view(),name="approve_sale"),
    path('get_product_selling_price/<product_id>/',views.get_product_selling_price,name="get_product_selling_price"),
    path('products/', views.ProductView.as_view(), name="products"),
    path('edit_product/<product_id>/',
         views.EditProductView.as_view(), name="edit_product"),
    path('delete_product/<product_id>/',
         views.delete_product, name="delete_product"),
    path('block_product/<product_id>/',
         views.block_product, name="block_product"),
    path('unblock_product/<product_id>/',
         views.unblock_product, name="unblock_product"),
    path('purchases/add/', views.AddPurchaseView.as_view(), name="add_purchase"),
    path('purchases/', views.PurchasesView.as_view(), name="purchases"),
    path('purchases/<pk>/', views.PurchasesView.as_view(), name="purchases"),
    path('purchases/<pk>/item/', views.AddPurchaseItemView.as_view(),
         name="add_purchase_item"),
    path('purchases/<pk>/item/remove', views.delete_purchase_item, name="remove_purchases_item"),
    path('purchases/<pk>/remove', views.delete_purchase, name="remove_purchases"),
    path('product/<pk>/short_name/',
         views.product_short_name, name="product_short_name"),
    path('expenses/', views.ExpenseView.as_view(), name="expenses"),
    path('expenses/<pk>/remove', views.delete_expense_item, name="remove_expenses"),
    path('expenses/<pk>/details', views.expense_detail_list, name="expenses_details"),
    path('customer_history/<pk>/', views.getCustomerHistory, name="customer_history"),
    path('customer_info/<pk>/', views.getCustomerInfo, name="customer_info"),
    path('remaining_product/<pk>/', views.getRemainingProduct, name="remaining_product"),

    path('stocks/', views.StockView.as_view(), name="stocks"),

    path('payments/', views.PaymentView.as_view(), name="payments"),
    path('customer_payment/', views.CustomerPaymentView.as_view(), name="customer_payment"),
    path('staff_collection/', views.StaffCollectionView.as_view(), name="staff_collection"),
    path('loan_collection/', views.LoanCollectionView.as_view(), name="loan_collection"),
    path('supplier_payment/', views.SupplierPaymentView.as_view(), name="supplier_payment"),
    path('other_payment/', views.OtherPaymentView.as_view(), name="other_payment"),
    path('loan_provision/', views.LoanProvisionView.as_view(), name="loan_provision"),
    path('staff_loan/', views.StaffLoanView.as_view(), name="staff_loan"),

    path('ror_calculator/', views.RORView.as_view(), name="ror_calculator"),
    path('edit_ror_commodity/<ror_id>', views.EditRORView.as_view(), name="edit_ror_commodity"),
    path('delete_ror_commodity/<ror_id>', views.delete_ror_commodity, name="delete_ror_commodity"),


    path('create/', views.CreateMovieView.as_view(), name='create'),
    path('update/', views.UpdateMovieView.as_view(), name='update'),

]
