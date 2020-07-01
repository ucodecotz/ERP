import datetime
from django import template
from control.models import UserProfile, Account, AccountTransaction, Attendance, Salary
from home.models import Product, Purchase, Sale, SaleItem, ExpenseDetail, Expense
from home.models import *
from control.customer_calculation import get_customer_debt, get_customer_credit_list
from control.staff_calculation import get_staff_loan, get_staff_loan_month
from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import timedelta
import calendar
from control.supplier_calculations import get_supplier_current_balance

register = template.Library()


@register.filter
def current_user_branch(user):
    user_obj = UserProfile.objects.filter(user=user).first()
    if user_obj.branch:
        return user_obj.branch.name
    else:
        return "No Branch"


@register.filter
def get_last_added_date(pk):
    product_obj = Product.objects.filter(id=pk).first()
    if Purchase.objects.filter(product=product_obj).last():
        date = Purchase.objects.filter(product=product_obj).last().created
    else:
        date = None
    return date


@register.filter
def get_last_added_purchase_price(pk):
    product_obj = Product.objects.filter(id=pk).first()
    if Purchase.objects.filter(product=product_obj).last():
        price = Purchase.objects.filter(
            product=product_obj).last().buying_price
    else:
        price = 0
    return price


@register.filter
def get_last_added_selling_price(pk):
    product_obj = Product.objects.filter(id=pk).first()
    if Purchase.objects.filter(product=product_obj).last():
        price = Purchase.objects.filter(
            product=product_obj).last().selling_price
    else:
        price = None
    return price


@register.filter
def get_total_expense_detail(pk):
    expense_details = ExpenseDetail.objects.filter(expense__id=pk)
    total = 0.0
    if expense_details:
        total = sum([s.expense_amount for s in expense_details])
    return total


@register.filter
def get_total_advance(pk, month):
    user_obj = UserProfile.objects.filter(id=pk).first()
    expenses_obj = Expense.objects.filter(staff=user_obj).filter(expense_date__year=datetime.now().year).filter(
        expense_date__month=int(month))
    expense_details = ExpenseDetail.objects.filter(
        expense__in=[s for s in expenses_obj])
    total = 0.0
    if expense_details:
        total = sum([s.expense_amount for s in expense_details])
    return float(total)


@register.filter
def get_ror(s_price, b_price):
    b_price = int(b_price)
    s_price = int(s_price)
    p_price = s_price - b_price
    ror = ((p_price / b_price) * 100)

    return round(ror, 2)


@register.filter
def customer_debt(pk):
    return get_customer_debt(pk)


@register.filter
def staff_loan(pk):
    return get_staff_loan(pk)


@register.filter
def staff_loan_month(pk, month):
    return get_staff_loan_month(pk, int(month))


@register.filter
def get_sale_items(sale):
    sale_items = SaleItem.objects.filter(sale__id=sale)
    return sale_items


@register.filter
def total_product_price(quantity, price):
    total = float(quantity) * float(price)
    return total


@register.filter
def total_sale_amount(sale):
    sale_items = SaleItem.objects.filter(
        sale__id=sale).values_list('quantity', 'price')
    if sale_items:
        total_amount = sum([float(s[0]) * float(s[1]) for s in sale_items])
    else:
        total_amount = 0
    return float(total_amount)


@register.filter
def total_expense_amount(expense):
    if ExpenseDetail.objects.filter(expense__id=expense).first():
        total_amount = ExpenseDetail.objects.filter(
            expense__id=expense).first().expense_amount
    else:
        total_amount = 0
    return total_amount


@register.filter
def total_account_amount(account):
    from control.account_calculations import total_account_amount
    total = total_account_amount(account)
    return total


@register.filter
def get_attendence_time(pk, date):
    user_obj = UserProfile.objects.filter(id=pk).first()
    if date:
        if Attendance.objects.filter(staff=user_obj.user).filter(
            created__day=date.day).filter(created__month=date.month).filter(
                created__year=date.year).exists():
            attendence_obj = Attendance.objects.filter(staff=user_obj.user).filter(
                created__day=date.day).filter(created__month=date.month).filter(
                created__year=date.year).first()
            time = attendence_obj.time_in
        else:
            time = None
    else:
        time = None
    return time


@register.filter
def get_attendence_comment(pk, date):
    user_obj = UserProfile.objects.filter(id=pk).first()
    if date:
        if Attendance.objects.filter(staff=user_obj.user).filter(
            created__day=date.day).filter(created__month=date.month).filter(
                created__year=date.year).exists():
            attendence_obj = Attendance.objects.filter(staff=user_obj.user).filter(
                created__day=date.day).filter(created__month=date.month).filter(
                created__year=date.year).first()
            comment = attendence_obj.comment
        else:
            comment = None
    comment = None
    return comment


@register.filter
def get_staff_sale_quantity(staff_id):
    staff = User.objects.filter(id=staff_id).first()
    total_sale_item = SaleItem.objects.filter(sale__staff=staff).values_list("quantity").aggregate(Sum("quantity"))[
        "quantity__sum"]
    if total_sale_item:
        total_sale_item = total_sale_item
    else:
        total_sale_item = 0
    return total_sale_item


@register.filter
def get_staff_sale_value(staff_id):
    staff = User.objects.filter(id=staff_id).first()
    total_amount = list()
    for sale in Sale.objects.filter(staff=staff):
        amount = total_sale_amount(sale.id)
        total_amount.append(amount)
    return float(sum(total_amount))


@register.filter
def total_profit_amount(sale):
    sale_obj = SaleItem.objects.filter(sale__id=sale)
    total_buying_price = list()
    for item in sale_obj:
        quantity = item.quantity
        buying_price = Purchase.objects.filter(
            product=item.product).first().buying_price
        total = float(quantity) * float(buying_price)
        total_buying_price.append(total)
    total_buying_amount = float(sum(total_buying_price))
    total_profit = float(total_sale_amount(sale)) - total_buying_amount
    return total_profit


@register.filter
def get_staff_sale_profit(staff_id):
    staff = User.objects.filter(id=staff_id).first()
    total_amount = list()
    for sale in Sale.objects.filter(staff=staff):
        profit = total_profit_amount(sale.id)
        total_amount.append(profit)
    profit = float(sum(total_amount))
    return profit


@register.filter
def get_debt_remainder(pk):
    return get_customer_credit_list(pk)


@register.filter
def get_debt_list_count(pk):
    count_list = list()
    for s in UserProfile.objects.filter(user_type="Customer"):
        for d in get_customer_credit_list(s.user.pk):
            count_list.append(d)
    return count_list


@register.filter
def calculate_remaining_days(pk, sale):
    user_obj = User.objects.filter(id=pk).first()
    userprofile_obj = UserProfile.objects.filter(user=user_obj).first()
    sale_obj = Sale.objects.filter(id=sale).first()
    my_date = sale_obj.sale_date.replace(tzinfo=None)
    now = datetime.now()
    if userprofile_obj.credit_day:
        credit_day = userprofile_obj.credit_day
    else:
        credit_day = 0
    if (my_date + timedelta(days=int(credit_day))) >= now:
        date = now - \
            (my_date + timedelta(days=int(credit_day)))
        date = "Remained: " + str(abs(date.days))
    else:
        date = (my_date + timedelta(days=int(credit_day))) - now
        date = "Exceed: " + str(abs(date.days))
    return date


@register.filter
def get_total_amount_staff_collected(staff_id):
    staff = User.objects.filter(id=staff_id).first()
    total_collected_amount = Payment.objects.filter(
        collected_by=staff).aggregate(Sum("amount"))["amount__sum"]
    if total_collected_amount:
        total_collected_amount = total_collected_amount
    else:
        total_collected_amount = 0.00
    return total_collected_amount


@register.filter
def get_sale_quantity(pk):
    sale_obj = Sale.objects.filter(id=pk).first()
    return SaleItem.objects.filter(sale=sale_obj).aggregate(Sum("quantity"))['quantity__sum']


@register.filter
def get_product_quantity_sold(product_id):
    product = Product.objects.filter(id=product_id).first()
    return SaleItem.objects.filter(product=product).aggregate(Sum("quantity"))['quantity__sum']


@register.filter
def get_sale_selling_price(pk):
    sale_obj = Sale.objects.filter(id=pk).first()
    value_items = SaleItem.objects.filter(sale=sale_obj).filter(
        is_active=True).values_list('quantity', 'price')
    return sum([float(s[0]) * float(s[1]) for s in value_items])


@register.filter
def get_product_reports(total_sales_items, pk):
    value_items = SaleItem.objects.filter(id__in=[s.pk for s in total_sales_items]).filter(
        is_active=True).filter(product__id=pk).values_list('quantity', 'product__id', 'price', 'sale__id')
    value_lists = list()
    sales_list = list()
    quantity_list = list()
    for s in value_items:
        sale_obj = Sale.objects.filter(id=s[3]).first()
        if Purchase.objects.filter(product__id=s[1]).filter(purchase_date__lte=sale_obj.sale_date).last():
            if Purchase.objects.filter(product__id=s[1]).filter(purchase_date__lte=sale_obj.sale_date).last():
                buying_price = Purchase.objects.filter(
                    product__id=s[1]).filter(purchase_date__lte=sale_obj.sale_date).last().buying_price
            else:
                buying_price = float(0)
            value_lists.append(s[0] * buying_price)
        selling_price = 0
        if s[2]:
            selling_price = s[2]
        sales_list.append(s[0]*selling_price)
        quantity_list.append(s[0])
    total_buying_price = sum(value_lists)
    total_selling_price = sum(sales_list)
    total_quantity = sum(quantity_list)
    profit = float(total_selling_price) - float(total_buying_price)
    return (total_buying_price, total_selling_price, profit, total_quantity)


@register.filter
def get_customer_product_quantity(total_sales_items, pk):
    customer_sale_list = list()
    for sale_item in SaleItem.objects.filter(id__in=[s.pk for s in total_sales_items]).filter(is_active=True).filter(product__id=pk):
        if sale_item.sale.customer:
            full_name = sale_item.sale.customer.first_name + " " + sale_item.sale.customer.last_name
        else:
            full_name = " "
        customer_sale_list.append({
            "date":  sale_item.sale.sale_date,
            "customer": full_name,
            "product": sale_item.product.name,
            "quantity": sale_item.quantity
        })
    return customer_sale_list


@register.filter
def get_sale_buying_price(pk):
    sale_obj = Sale.objects.filter(id=pk).first()
    value_items = SaleItem.objects.filter(sale=sale_obj).filter(
        is_active=True).values_list('quantity', 'product__id')
    value_lists = list()
    for s in value_items:
        if Purchase.objects.filter(product__id=s[1]).filter(purchase_date__lte=sale_obj.sale_date).last():
            if Purchase.objects.filter(product__id=s[1]).filter(purchase_date__lte=sale_obj.sale_date).last():
                buying_price = Purchase.objects.filter(
                    product__id=s[1]).filter(purchase_date__lte=sale_obj.sale_date).last().buying_price
            else:
                buying_price = 0
            value_lists.append(s[0] * buying_price)

    return sum(value_lists)


@register.filter
def get_sale_profit(pk):
    total = float(get_sale_selling_price(pk)) - \
        float(get_sale_buying_price(pk))
    return total


@register.filter
def get_cash_total(sales):
    sales = Sale.objects.filter(sale_type=True).filter(
        id__in=[s.pk for s in sales])
    return sum([get_sale_selling_price(s.pk) for s in sales])


@register.filter
def get_credit_total(sales):
    sales = Sale.objects.filter(sale_type=False).filter(
        id__in=[s.pk for s in sales])
    return sum([get_sale_selling_price(s.pk) for s in sales])


@register.filter
def get_product_capital(product_id):
    product = Product.objects.filter(id=product_id).first()
    quantiy = product.remaining_stock()
    b_price = get_last_added_purchase_price(product.pk)
    if quantiy > 0 and b_price > 0:
        total = float(quantiy * b_price)
    else:
        total = 0
    return total


@register.filter
def get_product_total_selling_price(product_id):
    product = Product.objects.filter(id=product_id).first()
    total_selling_price = SaleItem.objects.filter(
        product=product).aggregate(Sum("price"))['price__sum']
    return total_selling_price


@register.filter
def get_product_profit(product_id):
    quantity_sold = get_product_quantity_sold(product_id)
    sales = get_product_total_selling_price(product_id)
    if quantity_sold and sales:
        profit = float(quantity_sold * sales)
    else:
        profit = 0
    return profit


@register.filter
def get_deduction_amount(pk):
    user_obj = User.objects.filter(id=pk).first()
    if Payment.objects.filter(user=user_obj).filter(payment_type="staff loan").first():
        deduction_amount = Payment.objects.filter(user=user_obj).filter(
            payment_type="staff loan").first().deduction_amount
    else:
        deduction_amount = 0
    return deduction_amount


@register.simple_tag
def get_staff_net_pay(pk, deduction, month):
    user_obj = UserProfile.objects.filter(id=pk).first()
    total = 0
    if deduction:
        deduction = deduction
    else:
        deduction = 0
    if user_obj:
        total = float(user_obj.salary_amount) - \
            (get_total_advance(user_obj.pk, month) + float(deduction))
    return total


@register.filter
def month_name(month_number):
    return calendar.month_name[int(month_number)]


@register.filter
def check_payment_status(pk, month):
    user_obj = User.objects.filter(id=pk).first()
    return Salary.objects.filter(created__year=datetime.now().year).filter(staff=user_obj).filter(salary_date__month=month)

@register.filter
def get_supplier_total_balance(supplier_id):
    return get_supplier_current_balance(supplier_id)

@register.filter
def get_borrower_total_balance(borrower_id):   
    if UserProfile.objects.filter(user__id=borrower_id).first().balance:
        borrower_opening_balance = UserProfile.objects.filter(user__id=borrower_id).first().balance
    else:
        borrower_opening_balance = 0
    
    if Payment.objects.filter(user__id=borrower_id,payment_type="loan provision").exists():
        total_borrower_loans = Payment.objects.filter(user__id=borrower_id,payment_type="loan provision").aggregate(Sum('amount'))['amount__sum']
    else:
        total_borrower_loans = 0

    if Payment.objects.filter(user__id=borrower_id,payment_type="loan collection").exists():
        total_borrower_loan_payments = Payment.objects.filter(user__id=borrower_id,payment_type="loan collection").aggregate(Sum('amount'))['amount__sum']
    else:
        total_borrower_loan_payments = 0

    total_borrower_balance = float(borrower_opening_balance) + float(total_borrower_loans) - float(total_borrower_loan_payments)
    return total_borrower_balance
