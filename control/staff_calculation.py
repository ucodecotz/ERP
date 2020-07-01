from django.contrib.auth.models import User
from django.db.models import Sum

from control.models import UserProfile, SalaryDeduction
from home.models import BadDebt, Payment
from datetime import datetime

def get_staff_loan(pk):
    user_obj = User.objects.filter(id=pk).filter(is_superuser=False).first()
    user_profile_obj = UserProfile.objects.filter(user=user_obj).first()
    if BadDebt.objects.filter(staff=user_profile_obj):
        total_bad_debt = float(
            BadDebt.objects.filter(staff=user_profile_obj).aggregate(Sum('amount'))['amount__sum'])
    else:
        total_bad_debt = 0
    if Payment.objects.filter(payment_type="staff loan").filter(user=user_obj):
        total_payments = float(
            Payment.objects.filter(payment_type="staff loan").filter(user=user_obj).aggregate(Sum('amount'))[
                'amount__sum'])
    else:
        total_payments = 0

    if Payment.objects.filter(payment_type="staff collection").filter(user=user_obj):
        total_payments_collection = float(
            Payment.objects.filter(payment_type="staff collection").filter(user=user_obj).aggregate(Sum('amount'))[
                'amount__sum'])
    else:
        total_payments_collection = 0
    if SalaryDeduction.objects.filter(salary__staff=user_obj):
        total_deduction = float(SalaryDeduction.objects.filter(salary__staff=user_obj).aggregate(Sum('amount'))['amount__sum'])
    else:
        total_deduction = 0
    if user_profile_obj:
        if user_profile_obj.balance:
            staff_opening_balance = float(user_profile_obj.balance)
        else:
            staff_opening_balance = 0
    else:
        staff_opening_balance = 0
    loan = (total_bad_debt + total_payments + staff_opening_balance) - total_payments_collection
    total_loan = loan - total_deduction
    if total_loan < 0:
        total_loan = 0
    return total_loan


def get_staff_loan_month(pk, month):
    user_obj = User.objects.filter(id=pk).filter(is_superuser=False).first()
    user_profile_obj = UserProfile.objects.filter(user=user_obj).first()
    if BadDebt.objects.filter(staff=user_profile_obj):
        total_bad_debt = float(
            BadDebt.objects.filter(staff=user_profile_obj).aggregate(Sum('amount'))['amount__sum'])
    else:
        total_bad_debt = 0
    if Payment.objects.filter(payment_type="staff loan").filter(user=user_obj):
        total_payments = float(
            Payment.objects.filter(payment_type="staff loan").filter(user=user_obj).aggregate(Sum('amount'))[
                'amount__sum'])
    else:
        total_payments = 0

    if Payment.objects.filter(payment_type="staff collection").filter(user=user_obj):
        total_payments_collection = float(
            Payment.objects.filter(payment_type="staff collection").filter(user=user_obj).aggregate(Sum('amount'))[
                'amount__sum'])
    else:
        total_payments_collection = 0
    if SalaryDeduction.objects.filter(salary__staff=user_obj).filter(created__year=datetime.now().year).filter(created__month=month):
        total_deduction = float(SalaryDeduction.objects.filter(salary__staff=user_obj).filter(
            created__year=datetime.now().year).filter(created__month=month).aggregate(Sum('amount'))['amount__sum'])
    else:
        total_deduction = 0
    loan = (total_bad_debt + total_payments) - total_payments_collection
    total_loan = loan - total_deduction
    if total_loan < 0:
        total_loan = 0
    return total_loan
