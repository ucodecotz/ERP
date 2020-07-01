from django.contrib.auth.models import User
from django.db.models import Sum

from control.models import UserProfile
from home.models import Sale, SaleItem, Payment, BadDebt


def get_customer_debt(pk):
    user_obj = User.objects.filter(id=pk).first()
    userprofile_obj = UserProfile.objects.filter(user=user_obj).first()
    value_list_for_items = SaleItem.objects.filter(
        sale__in=[s for s in Sale.objects.filter(customer=user_obj).filter(sale_type=False)]).values_list('quantity',
                                                                                                          'price')
    total_credit_sales = sum(float(s[0]) * float(s[1]) for s in value_list_for_items)
    if Payment.objects.filter(payment_type="customer payment").filter(user=user_obj):
        total_payments = float(
            Payment.objects.filter(payment_type="customer payment").filter(user=user_obj).aggregate(Sum('amount'))[
                'amount__sum'])
    else:
        total_payments = 0
    if BadDebt.objects.filter(customer=userprofile_obj):
        total_bad_debt = float(BadDebt.objects.filter(customer=userprofile_obj).aggregate(Sum('amount'))['amount__sum'])
    else:
        total_bad_debt = 0
    if userprofile_obj.balance:
        customer_opening_balance = float(userprofile_obj.balance)
    else:
        customer_opening_balance = 0
    customer_debt = float((total_credit_sales + customer_opening_balance) - (total_payments + total_bad_debt))
    return customer_debt


def get_customer_credit_list(pk):
    user_obj = User.objects.filter(id=pk).first()
    userprofile_obj = UserProfile.objects.filter(user=user_obj).first()
    sales_list = Sale.objects.filter(customer=user_obj).filter(sale_type=False).filter(waiting_approval=False).order_by('sale_date')
    if Payment.objects.filter(payment_type="customer payment").filter(user=user_obj):
        total_payments = float(
            Payment.objects.filter(payment_type="customer payment").filter(user=user_obj).aggregate(Sum('amount'))[
                'amount__sum'])
    else:
        total_payments = 0
    if BadDebt.objects.filter(customer=userprofile_obj):
        total_bad_debt = float(BadDebt.objects.filter(customer=userprofile_obj).aggregate(Sum('amount'))['amount__sum'])
    else:
        total_bad_debt = 0
    balance = total_payments + total_bad_debt
    credit_list = list()
    for sale in sales_list:
        total_sale_amount = SaleItem.objects.filter(sale=sale).values_list('quantity', 'price')
        total_credit_saleItem = sum(float(s[0]) * float(s[1]) for s in total_sale_amount)
        if balance > 0:
            if balance > total_credit_saleItem:
                balance = balance - total_credit_saleItem
                if balance < 0:
                    credit_list.append(sale)
            else:
                credit_list.append(sale)
        else:
            credit_list.append(sale)
    return credit_list
