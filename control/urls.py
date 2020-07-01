from django.urls import path
from django.conf import global_settings
from control import views

urlpatterns = [
    path('assets/', views.AssetView.as_view(), name="assets"),
    path('edit_asset/<asset_id>/', views.EditAssetView.as_view(), name="edit_asset"),
    path('delete_asset/<asset_id>/', views.delete_asset, name="delete_asset"),

    path('regions/', views.RegionView.as_view(), name="regions"),
    path('edit_region/<region_id>/', views.EditRegionView.as_view(), name="edit_region"),
    path('delete_region/<region_id>/', views.delete_region, name="delete_region"),

    path('user_types/', views.UserTypeView.as_view(), name="user_types"),
    path("edit_user_type/<user_type_id>/", views.EditUserTypeView.as_view(), name="edit_user_type"),
    path('delete_user_type/<user_type_id>/', views.delete_user_type, name="delete_user_type"),

    path('branches/', views.BranchView.as_view(), name="branches"),
    path('edit_branch/<branch_id>/', views.EditBranchView.as_view(), name="edit_branch"),
    path('delete_branch/<branch_id>/', views.delete_branch, name="delete_branch"),

    path('user_profile/', views.userprofile, name="user_profile"),
    path('update_profile_info/', views.UpdateProfileInfoView.as_view(), name="update_profile_info"),
    path('change_password/', views.ChangePasswordView.as_view(), name="change_password"),

    path('payroll/', views.Payroll.as_view(), name="payroll"),
    path("salary_payment/", views.SalaryPaymentView.as_view(), name="salary_payment"),

    path('all_accounts/', views.AccountsView.as_view(), name="all_accounts"),
    path('add_account/', views.AddAccountView.as_view(), name="add_account"),
    path('edit_account/<account_id>/', views.EditAccountView.as_view(), name="edit_account"),
    path('delete_account/<account_id>/', views.delete_account, name="delete_account"),
    path('account_transactions/<account_id>/', views.AccountTransactionsView.as_view(), name="account_transactions"),
    path('account_deposit/<account_id>/', views.AccountDepositView.as_view(), name="account_deposit"),
    path('account_transfer/<account_id>/', views.AccountTransferView.as_view(), name="account_transfer"),
    path('cash_collection_transfer/',views.CashCollectionTransferView.as_view(),name="cash_collection_transfer"),
     
    path('notepad/', views.NotePadView.as_view(), name="notepad"),
    path('add_note/', views.AddNote.as_view(), name="add_note"),
    path('edit_note/<note_id>/', views.EditNote.as_view(), name="edit_note"),
    path('delete_note/<note_id>/', views.delete_note, name="delete_note"),

    path('sales_info/<sale_id>/', views.CustomerDebtReminderInfo.as_view(), name="sales_info"),

    path('attendence/', views.AttendenceView.as_view(), name="attendence"),
    path('attendence/form/', views.AttendenceFormView.as_view(), name="attendence_form"),
    path('sales_performance/', views.SalePerformanceView.as_view(), name="sales_performance"),
    path('staff_sale_detail/<staff_id>/',views.StaffSaleDetailView.as_view(),name="staff_sale_detail"),
    path('collection_performance/', views.CollectionPerformanceView.as_view(), name="collection_performance"),
    path('staff_collection_detail/', views.StaffCollectionDetailView.as_view(), name="staff_collection_detail"),
    path('monthly_employee_assesment/', views.MonthlyEmployeeAssesmentView.as_view(),
         name="monthly_employee_assesment"),
    path('staff_monthly_employee_assesment/<pk>/', views.StaffMonthlyEmployeeAssementDetailView.as_view(),
         name="staff_monthly_employee_assesment"),
    path('staff_collection_detail/<staff_id>/', views.StaffCollectionDetailView.as_view(),
         name="staff_collection_detail"),
    path('get_salary_month/', views.get_salary_month,
         name="get_salary_month"),
]
