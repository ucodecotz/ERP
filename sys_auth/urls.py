from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import global_settings
from sys_auth import views

urlpatterns = [
    path('users/',views.UsersView.as_view(),name="users"),

    path('add_customer/',views.AddCustomerView.as_view(),name="add_customer"),
    path('edit_customer/<customer_id>/',views.EditCustomerView.as_view(),name="edit_customer"),
    path('block_customer/<customer_id>/',views.block_customer,name="block_customer"),
    path('unblock_customer/<customer_id>/',views.unblock_customer,name="unblock_customer"),
    path('delete_customer/<customer_id>/',views.delete_customer,name="delete_customer"),
    path('bad_debt/<customer_id>/',views.BadDebtView.as_view(),name="bad_debt"),

    path('add_supplier/',views.AddSupplierView.as_view(),name="add_supplier"),
    path('edit_supplier/<supplier_id>/',views.EditSupplierView.as_view(),name="edit_supplier"),
    path('block_supplier/<supplier_id>/',views.block_supplier,name="block_supplier"),
    path('unblock_supplier/<supplier_id>/',views.unblock_supplier,name="unblock_supplier"),
    path('delete_supplier/<supplier_id>/',views.delete_supplier,name="delete_supplier"),

    path('add_borrower/',views.AddBorrowerView.as_view(),name="add_borrower"),
    path('edit_borrower/<borrower_id>/',views.EditBorrowerView.as_view(),name="edit_borrower"),
    path('block_borrower/<borrower_id>/',views.block_borrower,name="block_borrower"),
    path('unblock_borrower/<borrower_id>/',views.unblock_borrower,name="unblock_borrower"),
    path('delete_borrower/<borrower_id>/',views.delete_borrower,name="delete_borrower"),

    path('add_staff',views.AddStaffView.as_view(),name="add_staff"),
    path('edit_staff/<staff_id>/',views.EditStaffView.as_view(),name="edit_staff"),
    path('recover_staff_password/<staff_id>/',views.RecoverStaffPasswordView.as_view(),name="recover_staff_password"),
    path('block_staff/<staff_id>/',views.block_staff,name="block_staff"),
    path('unblock_staff/<staff_id>/',views.unblock_staff,name="unblock_staff"),
    path('delete_staff/<staff_id>/',views.delete_staff,name="delete_staff"),

    path('login/', views.LogInForm.as_view(), name='login'),
    path('logout/', views.logout_view, name="logout"),

    path('user_groups/',views.UserGroupView.as_view(),name="user_groups"),
    path('edit_user_group/<group_id>/',views.EditUserGroupView.as_view(),name="edit_user_group"),
    path('delete_group/<group_id>/',views.delete_group,name="delete_group"),
    path('group_permissions/<group_id>/',views.group_permissions,name="group_permissions"),
    path('assign_group_permission/<perm_id>/<group_id>/',views.assign_group_permission,name="assign_group_permission"),
    path('remove_group_permission/<perm_id>/<group_id>/',views.remove_group_permission,name="remove_group_permission"),
    path('group_staffs/<group_id>/',views.group_staffs,name="group_staffs"),
    path('assign_staff_group/<staff_id>/<group_id>/',views.assign_staff_group,name="assign_staff_group"),
    path('remove_staff_group/<staff_id>/<group_id>/',views.remove_staff_group,name="remove_staff_group"),


    path('customer_details/<customer_id>/',views.CustomerDetails.as_view(),name="customer_details"),
    path('supplier_details/<supplier_id>/',views.SupplierDetails.as_view(),name="supplier_details"),
    path('borrower_details/<borrower_id>/',views.BorrowerDetails.as_view(),name="borrower_details"),
]
