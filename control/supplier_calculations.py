from django.contrib.auth.models import User
from django.db.models import Sum

from control.models import UserProfile
from home.models import Purchase, Payment


def get_supplier_current_balance(supplier_id):
    if Purchase.objects.filter(supplier__id=supplier_id,purchase_type=False).exists():
        value_list_for_purchase = Purchase.objects.filter(supplier__id=supplier_id,purchase_type=False).values_list("quantity","buying_price")
        total_purchase_amount = sum(float(s[0]) * float(s[1]) for s in value_list_for_purchase)
    else:
        total_purchase_amount = 0
    
    if UserProfile.objects.filter(user__id=supplier_id).exists():
        if UserProfile.objects.filter(user__id=supplier_id).first().balance == None or UserProfile.objects.filter(user__id=supplier_id).first().balance == '':
            supplier_opening_balance = 0
        else:
            supplier_opening_balance = int(UserProfile.objects.filter(user__id=supplier_id).first().balance)
    else:
        supplier_opening_balance = 0
    
    if Payment.objects.filter(user__id=supplier_id,payment_type="supplier payment").exists():
        total_supplier_payments = Payment.objects.filter(user__id=supplier_id,payment_type="supplier payment").aggregate(Sum('amount'))['amount__sum']
    else:
        total_supplier_payments = 0
    
    total_supplier_balance = float(total_purchase_amount) + float(supplier_opening_balance) - float(total_supplier_payments)
    return total_supplier_balance