from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.conf import settings
from django.utils.dateparse import parse_date
from django.db.models import Q, Sum
from control.models import *
from home.models import *
import datetime
import json

today = datetime.datetime.now().date()


class ExpenseReportView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ExpenseReportView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = 'Expense Report'
        branch = "all"
        period = datetime.datetime.now().month
        expenses = Expense.objects.filter(is_active=True).filter(expense_date__year=datetime.datetime.now().year).filter(
            expense_date__month=datetime.datetime.now().month).order_by("-id")
        if request.GET.get("branch"):
            branch = request.GET.get("branch")

        if request.GET.get("period") == "1":
            if not branch == "all":
                expenses = Expense.objects.filter(expense_date__year=datetime.datetime.now().year).filter(
                    expense_date__month=datetime.datetime.now().month).filter(expense_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                expenses = Expense.objects.filter(expense_date__year=datetime.datetime.now().year).filter(
                    expense_date__month=datetime.datetime.now().month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "2":
            today = datetime.datetime.now()
            weekday = today.weekday()
            date = datetime.datetime.today() - datetime.timedelta(weeks=1, days=weekday)
            print(date)
            if not branch == "all":
                expenses = Expense.objects.filter(expense_date__gte=date.date()).filter(
                    expense_date__month__lte=datetime.datetime.today()).filter(expense_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                expenses = Sale.objects.filter(sale_date__date__gte=date.date()).filter(
                    sale_date__date__lte=datetime.datetime.today()).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "3":
            today = datetime.datetime.now().date()
            first = today.replace(day=1)
            lastMonth = first - datetime.timedelta(days=1)
            if not branch == "all":
                expenses = Expense.objects.filter(expense_date__year=lastMonth.year).filter(
                    expense_date__month=lastMonth.month).filter(expense_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                expenses = Expense.objects.filter(expense_date__year=lastMonth.year).filter(
                    expense_date__month=lastMonth.month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "0":
            start_date = datetime.datetime.strptime(
                str(request.GET.get("start_date")).strip(), "%d %B, %Y").date()
            end_date = datetime.datetime.strptime(
                str(request.GET.get("end_date")).strip(), "%d %B, %Y").date()
            if not branch == "all":
                expenses = Expense.objects.filter(expense_date__lte=start_date).filter(
                    expense_date__gte=end_date).filter(expense_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                expenses = Expense.objects.filter(expense_date__lte=start_date).filter(
                    expense_date__gte=end_date).filter(is_active=True).order_by("-id")
        context = {
            'title': title,
            "branches": Branch.objects.filter(is_active=True),
            "expenses": expenses,
        }
        return render(request, 'pages/expense_report.html', context)


class ProductReportView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductReportView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = 'Product Report'
        branch = "all"
        period = datetime.datetime.now().month
        sales = Sale.objects.filter(is_active=True).filter(sale_date__year=datetime.datetime.now().year).filter(
            sale_date__month=datetime.datetime.now().month).order_by("-id")
        if request.GET.get("branch"):
            branch = request.GET.get("branch")

        if request.GET.get("period") == "1":
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__year=datetime.datetime.now().year).filter(
                    sale_date__month=datetime.datetime.now().month).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__year=datetime.datetime.now().year).filter(
                    sale_date__month=datetime.datetime.now().month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "2":
            today = datetime.datetime.now()
            weekday = today.weekday()
            date = datetime.datetime.today() - datetime.timedelta(weeks=1, days=weekday)
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__date__gte=date.date()).filter(
                    sale_date__date__date__lte=datetime.datetime.today()).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__date__gte=date.date()).filter(
                    sale_date__date__lte=datetime.datetime.today()).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "3":
            today = datetime.datetime.now().date()
            first = today.replace(day=1)
            lastMonth = first - datetime.timedelta(days=1)
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__year=lastMonth.year).filter(
                    sale_date__month=lastMonth.month).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__year=lastMonth.year).filter(
                    sale_date__month=lastMonth.month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "0":
            start_date = datetime.datetime.strptime(
                str(request.GET.get("start_date")).strip(), "%d %B, %Y").date()
            end_date = datetime.datetime.strptime(
                str(request.GET.get("end_date")).strip(), "%d %B, %Y").date()
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__date__gte=start_date).filter(
                    sale_date__date__lte=end_date).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__date__gte=start_date).filter(
                    sale_date__date__lte=end_date).filter(is_active=True).order_by("-id")
        product_list = list()
        branches = Branch.objects.filter(is_active=True)
        customer_sale_list = list()
        total_sales_items = list()
        for sale in sales:
            sale_items = SaleItem.objects.filter(sale=sale)
            if sale.customer:
                full_name = sale.customer.first_name + " " + sale.customer.last_name
            else:
                full_name = " "
            quantity_list = list()
            for sale_item in sale_items:
                total_sales_items.append(sale_item)
                product_list.append(sale_item.product)
                quantity_list.append(sale_item.quantity)

                customer_sale_list.append({
                    "id":  sale_item.product.id,
                    "customer": full_name,
                    "product": sale_item.product.name,
                    "quantity": sale_item.quantity
                })
        context = {
            'title': title,
            'products': list(set(product_list)),
            'branches': branches,
            'period': period,
            'branch': branch,
            "customer_sale_list": customer_sale_list,
            "total_sales_items": total_sales_items
        }
        return render(request, 'pages/product_report.html', context)


class PurchaseReportView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PurchaseReportView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = 'Purchase Report'
        branch = "all"
        period = datetime.datetime.now().month

        purchases = Purchase.objects.filter(is_active=True).filter(purchase_date__year=datetime.datetime.now().year).filter(
            purchase_date__month=datetime.datetime.now().month).order_by("-id")

        if request.GET.get("branch"):
            branch = request.GET.get("branch")

        if request.GET.get("period") == "1":
            if not branch == "all":
                purchases = Purchase.objects.filter(purchase_date__year=datetime.datetime.now().year).filter(
                    purchase_date__month=datetime.datetime.now().month).filter(purchase_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                purchases = Purchase.objects.filter(purchase_date__year=datetime.datetime.now().year).filter(
                    purchase_date__month=datetime.datetime.now().month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "2":
            today = datetime.datetime.now()
            weekday = today.weekday()
            date = datetime.datetime.today() - datetime.timedelta(weeks=1, days=weekday)
            if not branch == "all":
                purchases = Purchase.objects.filter(purchase_date__date__gte=date.date()).filter(
                    purchase_date__lte=datetime.datetime.today()).filter(purchase_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                purchases = Purchase.objects.filter(purchase_date__date__gte=date.date()).filter(
                    purchase_date__lte=datetime.datetime.today()).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "3":
            today = datetime.datetime.now().date()
            first = today.replace(day=1)
            lastMonth = first - datetime.timedelta(days=1)
            if not branch == "all":
                purchases = Purchase.objects.filter(purchase_date__year=lastMonth.year).filter(
                    purchase_date__month=lastMonth.month).filter(purchase_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                purchases = Purchase.objects.filter(purchase_date__year=lastMonth.year).filter(
                    purchase_date__month=lastMonth.month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "0":
            start_date = datetime.datetime.strptime(
                str(request.GET.get("start_date")).strip(), "%d %B, %Y").date()
            end_date = datetime.datetime.strptime(
                str(request.GET.get("end_date")).strip(), "%d %B, %Y").date()
            if not branch == "all":
                purchases = Sale.objects.filter(purchase_date__gte=start_date).filter(
                    purchase_date__lte=end_date).filter(purchase_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                purchases = Purchase.objects.filter(purchase_date__gte=start_date).filter(
                    purchase_date__lte=end_date).filter(is_active=True).order_by("-id")
        context = {
            'title': title,
            "branches": Branch.objects.filter(is_active=True),
            "purchases": purchases,
        }
        return render(request, 'pages/purchase_report.html', context)


class SalesReportView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SalesReportView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = 'Sales Report'
        branch = "all"
        period = datetime.datetime.now().month

        sales = Sale.objects.filter(is_active=True).filter(sale_date__year=datetime.datetime.now().year).filter(
            sale_date__month=datetime.datetime.now().month).order_by("-id")

        if request.GET.get("branch"):
            branch = request.GET.get("branch")

        if request.GET.get("period") == "1":
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__year=datetime.datetime.now().year).filter(
                    sale_date__month=datetime.datetime.now().month).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__year=datetime.datetime.now().year).filter(
                    sale_date__month=datetime.datetime.now().month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "2":
            today = datetime.datetime.now()
            weekday = today.weekday()
            date = datetime.datetime.today() - datetime.timedelta(weeks=1, days=weekday)
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__date__gte=date.date()).filter(
                    sale_date__date__date__lte=datetime.datetime.today()).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__date__gte=date.date()).filter(
                    sale_date__date__lte=datetime.datetime.today()).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "3":
            today = datetime.datetime.now().date()
            first = today.replace(day=1)
            lastMonth = first - datetime.timedelta(days=1)
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__year=lastMonth.year).filter(
                    sale_date__month=lastMonth.month).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__year=lastMonth.year).filter(
                    sale_date__month=lastMonth.month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "0":
            start_date = datetime.datetime.strptime(
                str(request.GET.get("start_date")).strip(), "%d %B, %Y").date()
            end_date = datetime.datetime.strptime(
                str(request.GET.get("end_date")).strip(), "%d %B, %Y").date()
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__date__gte=start_date).filter(
                    sale_date__date__lte=end_date).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__date__gte=start_date).filter(
                    sale_date__date__lte=end_date).filter(is_active=True).order_by("-id")
        total_sales_items = list()
        for sale in sales:
            sale_items = SaleItem.objects.filter(sale=sale)
            for sale_item in sale_items:
                total_sales_items.append(sale_item)
        context = {
            'title': title,
            "branches": Branch.objects.filter(is_active=True),
            "sales": sales,
            "total_sales_items": total_sales_items
        }
        return render(request, 'pages/sales_report.html', context)


class StockReportView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StockReportView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = 'Stock Report'
        products = Product.objects.all()
        context = {
            'title': title,
            'products': products,
        }
        return render(request, 'pages/stock_report.html', context)


class ProfitLossReportView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfitLossReportView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = 'Profit & Loss Report'
        branch = "all"
        period = datetime.datetime.now().month
        sales = Sale.objects.filter(is_active=True).filter(sale_date__year=datetime.datetime.now().year).filter(
            sale_date__month=datetime.datetime.now().month).order_by("-id")
        if request.GET.get("branch"):
            branch = request.GET.get("branch")

        if request.GET.get("period") == "1":
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__year=datetime.datetime.now().year).filter(
                    sale_date__month=datetime.datetime.now().month).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__year=datetime.datetime.now().year).filter(
                    sale_date__month=datetime.datetime.now().month).filter(is_active=True).order_by("-id")

            if not branch == "all":
                expenses = Expense.objects.filter(expense_date__year=datetime.datetime.now().year).filter(
                    expense_date__month=datetime.datetime.now().month).filter(expense_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                expenses = Expense.objects.filter(expense_date__year=datetime.datetime.now().year).filter(
                    expense_date__month=datetime.datetime.now().month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "2":
            today = datetime.datetime.now()
            weekday = today.weekday()
            date = datetime.datetime.today() - datetime.timedelta(weeks=1, days=weekday)
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__date__gte=date.date()).filter(
                    sale_date__date__lte=datetime.datetime.today()).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__date__gte=date.date()).filter(
                    sale_date__date__date__lte=datetime.datetime.today()).filter(is_active=True).order_by("-id")
            if not branch == "all":
                expenses = Expense.objects.filter(expense_date__gte=date.date()).filter(
                    expense_date__month__lte=datetime.datetime.today()).filter(expense_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                expenses = Sale.objects.filter(sale_date__date__gte=date.date()).filter(
                    sale_date__date__lte=datetime.datetime.today()).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "3":
            today = datetime.datetime.now().date()
            first = today.replace(day=1)
            lastMonth = first - datetime.timedelta(days=1)
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__year=lastMonth.year).filter(
                    sale_date__month=lastMonth.month).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__year=lastMonth.year).filter(
                    sale_date__month=lastMonth.month).filter(is_active=True).order_by("-id")
            if not branch == "all":
                expenses = Expense.objects.filter(expense_date__year=lastMonth.year).filter(
                    expense_date__month=lastMonth.month).filter(expense_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                expenses = Expense.objects.filter(expense_date__year=lastMonth.year).filter(
                    expense_date__month=lastMonth.month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "0":
            start_date = datetime.datetime.strptime(
                str(request.GET.get("start_date")).strip(), "%d %B, %Y").date()
            end_date = datetime.datetime.strptime(
                str(request.GET.get("end_date")).strip(), "%d %B, %Y").date()
            if not branch == "all":
                sales = Sale.objects.filter(sale_date__date__gte=start_date).filter(
                    sale_date__date__lte=end_date).filter(sale_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                sales = Sale.objects.filter(sale_date__date__gte=start_date).filter(
                    sale_date__date__lte=end_date).filter(is_active=True).order_by("-id")

            start_date = datetime.datetime.strptime(
                str(request.GET.get("start_date")).strip(), "%d %B, %Y").date()
            end_date = datetime.datetime.strptime(
                str(request.GET.get("end_date")).strip(), "%d %B, %Y").date()
            if not branch == "all":
                expenses = Expense.objects.filter(expense_date__lte=start_date).filter(
                    expense_date__gte=end_date).filter(expense_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                expenses = Expense.objects.filter(expense_date__lte=start_date).filter(
                    expense_date__gte=end_date).filter(is_active=True).order_by("-id")

        expenses = Expense.objects.filter(is_active=True).filter(expense_date__year=datetime.datetime.now().year).filter(
            expense_date__month=datetime.datetime.now().month).order_by("-id")

        value_list_for_items = SaleItem.objects.filter(
            sale__in=[s for s in sales]).values_list('quantity', 'price')
        total_sales = sum(float(s[0]) * float(s[1])
                          for s in value_list_for_items)
        total_expense = ExpenseDetail.objects.filter(
            expense__in=[s for s in expenses]).values_list('expense_amount')
        value_items = SaleItem.objects.filter(sale__in=[s for s in sales]).filter(
            is_active=True).values_list('quantity', 'product__id', 'sale__id')
        value_lists = list()
        for s in value_items:
            sale_obj = Sale.objects.filter(id=s[2]).first()
            if Purchase.objects.filter(product__id=s[1]).filter(purchase_date__lte=sale_obj.sale_date).last():
                if Purchase.objects.filter(product__id=s[1]).filter(purchase_date__lte=sale_obj.sale_date).last():
                    buying_price = Purchase.objects.filter(
                        product__id=s[1]).filter(purchase_date__lte=sale_obj.sale_date).last().buying_price
                else:
                    buying_price = 0
                value_lists.append(s[0] * buying_price)
        total_expense = sum(s[0] for s in total_expense)
        total_cost_of_goods = sum(value_lists)
        gross_profit = float(total_sales) - float(total_cost_of_goods)
        net_profit = float(gross_profit) - float(total_expense)
        context = {
            'title': title,
            "total_sales": total_sales,
            "total_cost_of_goods": total_cost_of_goods,
            "gross_profit": gross_profit,
            "total_expense": total_expense,
            "net_profit": net_profit
        }
        return render(request, 'pages/profit_loss.html', context)


class DeleteSaleView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, sale_id):
        context = list()
        if Sale.objects.filter(id=sale_id).exists():
            Sale.objects.filter(id=sale_id).delete()
            if not Sale.objects.filter(id=sale_id).exists():
                info = {
                    'status': True,
                    'message': "Sale deleted succesfully"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to delete sale"
                }
        else:
            info = {
                'status': False,
                'message': "Sale does not exists"
            }
        context.append(info)
        return HttpResponse(json.dumps(context))


class PaymentReportView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        branch = "all"

        period = datetime.datetime.now().month

        payment_list = Payment.objects.filter(is_active=True).filter(payment_date__year=datetime.datetime.now().year).filter(
            payment_date__month=datetime.datetime.now().month).order_by("-id")

        if request.GET.get("branch"):
            branch = request.GET.get("branch")

        if request.GET.get("period") == "1":
            if not branch == "all":
                payment_list = Payment.objects.filter(payment_date__year=datetime.datetime.now().year).filter(
                    payment_date__month=datetime.datetime.now().month).filter(payment_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                payment_list = Payment.objects.filter(payment_date__year=datetime.datetime.now().year).filter(
                    payment_date__month=datetime.datetime.now().month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "2":
            today = datetime.datetime.now()
            weekday = today.weekday()
            date = datetime.datetime.today() - datetime.timedelta(weeks=1, days=weekday)
            if not branch == "all":
                payment_list = Payment.objects.filter(payment_date__date__gte=date.date()).filter(
                    payment_date__date__date__lte=datetime.datetime.today()).filter(payment_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                payment_list = Payment.objects.filter(payment_date__date__gte=date.date()).filter(
                    payment_date__date__date__lte=datetime.datetime.today()).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "3":
            today = datetime.datetime.now().date()
            first = today.replace(day=1)
            lastMonth = first - datetime.timedelta(days=1)
            if not branch == "all":
                payment_list = Payment.objects.filter(payment_date__year=lastMonth.year).filter(
                    payment_date__month=lastMonth.month).filter(payment_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                payment_list = Payment.objects.filter(payment_date__year=lastMonth.year).filter(
                    payment_date__month=lastMonth.month).filter(is_active=True).order_by("-id")
        elif request.GET.get("period") == "0":
            start_date = datetime.datetime.strptime(
                str(request.GET.get("start_date")).strip(), "%d %B, %Y").date()
            end_date = datetime.datetime.strptime(
                str(request.GET.get("end_date")).strip(), "%d %B, %Y").date()
            if not branch == "all":
                payment_list = Payment.objects.filter(payment_date__date__gte=start_date).filter(
                    payment_date__date__lte=end_date).filter(payment_branch__id=branch).filter(
                    is_active=True).order_by("-id")
            else:
                payment_list = Payment.objects.filter(payment_date__date__gte=start_date).filter(
                    payment_date__date__lte=end_date).filter(is_active=True).order_by("-id")
                

        context = {
            'title': 'Payment report',
            'payments': payment_list,
            'branches': Branch.objects.filter(is_active=True)
        }
        return render(request, 'pages/payment_report.html', context)


class DeletePaymentView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, payment_id):
        context = list()
        if Payment.objects.filter(id=payment_id).exists():
            Payment.objects.filter(id=payment_id).delete()
            if not Payment.objects.filter(id=payment_id).exists():
                info = {
                    'status': True,
                    'message': "Payment deleted succesfully"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to delete Payment"
                }
        else:
            info = {
                'status': False,
                'message': "Payment does not exists"
            }
        context.append(info)
        return HttpResponse(json.dumps(context))
