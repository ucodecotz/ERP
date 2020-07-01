from django.urls import path
from django.conf import global_settings
from report.views import *

urlpatterns = [
    path('expense_report/', ExpenseReportView.as_view(), name='expense_report'),
    path('product_report/', ProductReportView.as_view(), name='product_report'),
    path('purchase_report/', PurchaseReportView.as_view(), name='purchase_report'),
    path('payment_report/', PaymentReportView.as_view(), name='payment_report'),
    path('delete_payment/<int:payment_id>/',DeletePaymentView.as_view(),name="delete_payment"),
    path('sales_report/', SalesReportView.as_view(), name='sales_report'),
    path('stock_report/', StockReportView.as_view(), name='stock_report'),
    path('profit_loss/', ProfitLossReportView.as_view(), name='profit_loss'),
    path('delete_sale/<int:sale_id>/',DeleteSaleView.as_view(),name="delete_sale"),
]
