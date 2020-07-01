from control.models import AccountTransaction, Account
from home.models import Sale, SaleItem, Payment, Expense
from django.db.models import Q, Sum


def get_today_total_cash_amount():
    payments = list()
    payment_withdraws = list()
    payment_withdraws_and_transfer = list()
    for account in AccountTransaction.objects.all():
        if account.payments.first():
            payments.append(account.payments.first())
    for account in AccountTransaction.objects.filter(transanction_type="withdraw"):
        if account.payments.first():
            payment_withdraws.append(account.payments.first())
    for account in AccountTransaction.objects.filter(Q(transanction_type="withdraw")|Q(transanction_type="transfer")):
        if account.payments.first():
            payment_withdraws_and_transfer.append(account.payments.first())
    import datetime
    today = datetime.datetime.now().date()
    today_customer_cash_payments = Payment.objects.filter(payment_type="customer payment").filter(
        payment_date__date=today).exclude(id__in=[s.pk for s in payments]).aggregate(Sum("amount"))["amount__sum"]
    if today_customer_cash_payments:
        today_customer_cash_payments = today_customer_cash_payments
    else:
        today_customer_cash_payments = 0

    today_borrower_cash_payments = Payment.objects.filter(payment_type="loan collection").filter(
        payment_date__date=today).exclude(id__in=[s.pk for s in payments]).aggregate(Sum("amount"))["amount__sum"]
    if today_borrower_cash_payments:
        today_borrower_cash_payments = today_borrower_cash_payments
    else:
        today_borrower_cash_payments = 0

    today_cash_sales_payment = SaleItem.objects.filter(sale__in=[s for s in Sale.objects.filter(
        sale_date__date=today).filter(sale_type=True).exclude(id__in=[s.pk for s in payments])]).values_list('quantity', 'price')
    if today_cash_sales_payment:
        total_today_cash_sales_payment = sum(
            float(s[0]) * float(s[1]) for s in today_cash_sales_payment)
    else:
        total_today_cash_sales_payment = 0

    today_other_payments = Payment.objects.filter(payment_type="other payment").filter(
        payment_date__date=today).exclude(id__in=[s.pk for s in payment_withdraws_and_transfer]).aggregate(Sum("amount"))["amount__sum"]
    if today_other_payments:
        today_other_payments = today_other_payments
    else:
        today_other_payments = 0

    today_supplier_payments = Payment.objects.filter(payment_type="supplier payment").filter(
        payment_date__date=today).exclude(id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_supplier_payments:
        today_supplier_payments = today_supplier_payments
    else:
        today_supplier_payments = 0

    today_staff_loans = Payment.objects.filter(payment_type="staff loan").filter(
        payment_date__date=today).exclude(id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_staff_loans:
        today_staff_loans = today_staff_loans
    else:
        today_staff_loans = 0

    today_loan_provisions = Payment.objects.filter(payment_type="loan provision").filter(
        payment_date__date=today).exclude(id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_loan_provisions:
        today_loan_provisions = today_loan_provisions
    else:
        today_loan_provisions = 0

    total_cash_collection = float(today_customer_cash_payments) + float(today_borrower_cash_payments) + float(
        total_today_cash_sales_payment) - float(today_other_payments + today_supplier_payments + today_staff_loans + today_loan_provisions)
    return total_cash_collection


def get_today_total_bank_amount():
    payments = list()
    payment_withdraws = list()
    for account in AccountTransaction.objects.all():
        if account.payments.first():
            payments.append(account.payments.first())
    for account in AccountTransaction.objects.filter(transanction_type="withdraw"):
        if account.payments.first():
            payment_withdraws.append(account.payments.first())
    import datetime
    today = datetime.datetime.now().date()
    today_customer_cash_payments = Payment.objects.filter(payment_type="customer payment").filter(
        payment_date__date=today).filter(id__in=[s.pk for s in payments]).aggregate(Sum("amount"))["amount__sum"]
    if today_customer_cash_payments:
        today_customer_cash_payments = today_customer_cash_payments
    else:
        today_customer_cash_payments = 0

    today_borrower_cash_payments = Payment.objects.filter(payment_type="loan collection").filter(
        payment_date__date=today).filter(id__in=[s.pk for s in payments]).aggregate(Sum("amount"))["amount__sum"]
    if today_borrower_cash_payments:
        today_borrower_cash_payments = today_borrower_cash_payments
    else:
        today_borrower_cash_payments = 0

    today_cash_sales_payment = SaleItem.objects.filter(sale__in=[s for s in Sale.objects.filter(
        sale_date__date=today).filter(sale_type=True).filter(id__in=[s.pk for s in payments])]).values_list('quantity', 'price')
    if today_cash_sales_payment:
        total_today_cash_sales_payment = sum(
            float(s[0]) * float(s[1]) for s in today_cash_sales_payment)
    else:
        total_today_cash_sales_payment = 0

    today_other_payments = Payment.objects.filter(payment_type="other payment").filter(
        payment_date__date=today).filter(id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_other_payments:
        today_other_payments = today_other_payments
    else:
        today_other_payments = 0

    today_supplier_payments = Payment.objects.filter(payment_type="supplier payment").filter(
        payment_date__date=today).filter(id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_supplier_payments:
        today_supplier_payments = today_supplier_payments
    else:
        today_supplier_payments = 0

    today_staff_loans = Payment.objects.filter(payment_type="staff loan").filter(
        payment_date__date=today).filter(id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_staff_loans:
        today_staff_loans = today_staff_loans
    else:
        today_staff_loans = 0

    today_loan_provisions = Payment.objects.filter(payment_type="loan provision").filter(
        payment_date__date=today).filter(id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_loan_provisions:
        today_loan_provisions = today_loan_provisions
    else:
        today_loan_provisions = 0

    total_bank_collection = float(today_customer_cash_payments) + float(today_borrower_cash_payments) + float(
        total_today_cash_sales_payment) - float(today_other_payments + today_supplier_payments + today_staff_loans + today_loan_provisions)
    return total_bank_collection


def total_petty_account_amount():
    deposits = \
        AccountTransaction.objects.filter(account__name="PETTY CASH").filter(transanction_type="deposit").aggregate(Sum('amount'))[
            "amount__sum"]
    withdraws = \
        AccountTransaction.objects.filter(account__name="PETTY CASH").filter(transanction_type="withdraw").aggregate(Sum('amount'))[
            "amount__sum"]

    transfer = AccountTransaction.objects.filter(account__name="PETTY CASH").filter(
        transanction_type="transfer").aggregate(Sum('amount'))["amount__sum"]
    if deposits:
        deposits = deposits
    else:
        deposits = 0
    if withdraws:
        withdraws = withdraws
    else:
        withdraws = 0
    if transfer:
        transfer = transfer
    else:
        transfer = 0
    if Account.objects.filter(name="PETTY CASH").exists():
        opening_balance = float(Account.objects.filter(
            name="PETTY CASH").first().opening_balance)
    else:
        opening_balance = 0
    total = (float(deposits) + float(opening_balance) +
             float(transfer)) - float(withdraws)
    print(total)
    return total


def total_account_amount(account):
    deposits = \
        AccountTransaction.objects.filter(account__id=account).filter(transanction_type="deposit").aggregate(Sum('amount'))[
            "amount__sum"]
    withdraws = \
        AccountTransaction.objects.filter(account__id=account).filter(transanction_type="withdraw").aggregate(Sum('amount'))[
            "amount__sum"]
    transfer = AccountTransaction.objects.filter(account__id=account).filter(
        transanction_type="transfer").aggregate(Sum('amount'))["amount__sum"]
    if deposits:
        deposits = deposits
    else:
        deposits = 0
    if withdraws:
        withdraws = withdraws
    else:
        withdraws = 0
    if transfer:
        transfer = transfer
    else:
        transfer = 0
    if Account.objects.filter(id=account).first().opening_balance:
        opening_balance = float(Account.objects.filter(
            id=account).first().opening_balance)
    else:
        opening_balance = 0
    total = float(deposits) + float(opening_balance) + \
        float(transfer) - float(withdraws)
    return total


def get_all_accounts_amount_up_to_date():
    total = 0
    if Account.objects.filter(is_active=True).exists():
        for account in Account.objects.filter(is_active=True):
            if total_account_amount(account.id):
                total += total_account_amount(account.id)
    return float(total)


def get_total_cash_on_hand():
    payments = list()
    payment_withdraws = list()
    for account in AccountTransaction.objects.all():
        if account.payments.first():
            payments.append(account.payments.first())
    for account in AccountTransaction.objects.filter(transanction_type="withdraw"):
        if account.payments.first():
            payment_withdraws.append(account.payments.first())
    today_customer_cash_payments = Payment.objects.filter(payment_type="customer payment").exclude(
        id__in=[s.pk for s in payments]).aggregate(Sum("amount"))["amount__sum"]

    if today_customer_cash_payments:
        today_customer_cash_payments = today_customer_cash_payments
    else:
        today_customer_cash_payments = 0

    today_borrower_cash_payments = Payment.objects.filter(payment_type="loan collection").exclude(
        id__in=[s.pk for s in payments]).aggregate(Sum("amount"))["amount__sum"]
    if today_borrower_cash_payments:
        today_borrower_cash_payments = today_borrower_cash_payments
    else:
        today_borrower_cash_payments = 0

    today_cash_sales_payment = SaleItem.objects.filter(sale__in=[s for s in Sale.objects.filter(sale_type=True).exclude(
        id__in=[s.pk for s in payments])]).values_list('quantity', 'price')
    if today_cash_sales_payment:
        total_today_cash_sales_payment = sum(
            float(s[0]) * float(s[1]) for s in today_cash_sales_payment)
    else:
        total_today_cash_sales_payment = 0

    today_other_payments = Payment.objects.filter(payment_type="other payment").exclude(
        id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_other_payments:
        today_other_payments = today_other_payments
    else:
        today_other_payments = 0

    today_supplier_payments = Payment.objects.filter(payment_type="supplier payment").exclude(
        id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_supplier_payments:
        today_supplier_payments = today_supplier_payments
    else:
        today_supplier_payments = 0

    today_staff_loans = Payment.objects.filter(payment_type="staff loan").exclude(
        id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_staff_loans:
        today_staff_loans = today_staff_loans
    else:
        today_staff_loans = 0

    today_loan_provisions = Payment.objects.filter(payment_type="loan provision").exclude(
        id__in=[s.pk for s in payment_withdraws]).aggregate(Sum("amount"))["amount__sum"]
    if today_loan_provisions:
        today_loan_provisions = today_loan_provisions
    else:
        today_loan_provisions = 0

    total_cash_collection = float(today_customer_cash_payments) + float(today_borrower_cash_payments) + float(
        total_today_cash_sales_payment) - float(today_other_payments + today_supplier_payments + today_staff_loans + today_loan_provisions)
    return total_cash_collection