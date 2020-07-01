from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import View
from django.conf import settings
from django.utils.dateparse import parse_date
from django.db.models import Q, Sum
import json

from control.templatetags.control_filters import get_total_expense_detail
from home.forms import *
from control.models import UserProfile, Branch
from .forms import *
import datetime
from datetime import date
import itertools
from control.customer_calculation import get_customer_debt
from control.templatetags import control_filters


class HomeView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        today = datetime.datetime.now().date()
        today_sales = SaleItem.objects.filter(sale__in=[s for s in Sale.objects.filter(
            sale_date__date=today)]).values_list('quantity', 'price')
        if today_sales:
            total_today_sales = sum(
                float(s[0]) * float(s[1]) for s in today_sales)
        else:
            total_today_sales = 0
        today_expenses = ExpenseDetail.objects.filter(expense__expense_date=today).aggregate(
            Sum("expense_amount"))["expense_amount__sum"]
        if today_expenses:
            today_total_expenses = today_expenses
        else:
            today_total_expenses = 0
        today_sale_list = Sale.objects.filter(
            sale_date__date=today).order_by("-created")
        today_expense_list = Expense.objects.filter(
            expense_date=today).order_by("created")
        from control.account_calculations import get_today_total_cash_amount,get_today_total_bank_amount,total_petty_account_amount,get_total_cash_on_hand
        context = {
            'title': "Home",
            'total_today_sales': total_today_sales,
            'today_total_expenses': today_total_expenses,
            'total_cash_collection': get_today_total_cash_amount(),
            'total_bank_collection': get_today_total_bank_amount(),
            'total_collection': get_today_total_cash_amount() + get_today_total_bank_amount(),
            'coh': get_total_cash_on_hand(),
            'sale_list': today_sale_list,
            'expense_list': today_expense_list,
            'petty_cash_account': total_petty_account_amount(),
        }
        return render(request, 'pages/home.html', context)


@never_cache
@login_required(login_url="/auth/login/")
def getCustomerHistory(request, *args, **kwargs):
    sale_list = list()
    user_profile_obj = UserProfile.objects.filter(id=kwargs.get("pk")).first()
    for sale in Sale.objects.filter(customer=user_profile_obj.user).filter(is_active=True).order_by("-id")[:4]:
        total_items = []
        for item in SaleItem.objects.filter(sale=sale):
            total = float(item.price) * float(item.quantity)
            total_items.append(total)
        sale_list.append({
            "date": sale.sale_date,
            "amount": sum(total_items)
        })
    context = {
        "sale_list": sale_list
    }
    return render(request, "common/customer_history.html", context)


@never_cache
@login_required(login_url="/auth/login/")
def getRemainingProduct(request, *args, **kwargs):
    context = list()
    product = Product.objects.filter(id=kwargs.get("pk")).first()
    purchase_obj = Purchase.objects.filter(
        product=product).order_by("-updated").first()
    total = Purchase.objects.filter(product=product).aggregate(
        Sum('quantity'))['quantity__sum']
    if not total:
        total = 0
    total_sold_product = SaleItem.objects.filter(
        product=product).aggregate(Sum('quantity'))['quantity__sum']
    if not total_sold_product:
        total_sold_product = 0
    if purchase_obj:
        selling_price = purchase_obj.selling_price
    else:
        selling_price = 0
    info = {
        "total": total - total_sold_product,
        "selling_price": int(selling_price)
    }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login/")
def getCustomerInfo(request, *args, **kwargs):
    context = list()
    customer = UserProfile.objects.filter(id=kwargs.get("pk")).first().user
    print(customer)
    if customer.first_name and customer.last_name:
        name = customer.first_name + " " + customer.last_name
    else:
        name = customer.username
    userProfile = UserProfile.objects.filter(user=customer).first()
    if userProfile:
        credit_limit = userProfile.credit_limit
        balance = userProfile.balance
    else:
        credit_limit = 0.0
        balance = 0.0
    info = {
        "name": name,
        "credit_limit": credit_limit,
        'balance': get_customer_debt(customer.pk),
    }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login/")
def get_product_selling_price(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    purchase = Purchase.objects.filter(product=product).order_by(
        "-updated").first().selling_price
    info = {
        'selling_price': str(purchase),
    }
    return HttpResponse(json.dumps(info))


class AddSalesView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddSalesView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = SalesForm()
        context = {
            'title': "Add Sales",
            'sysname': settings.SYS_NAME,
            "form": form,
        }
        return render(request, 'pages/add_sales.html', context)

    def post(self, request, *args, **kwargs):
        context = list()
        form = SalesForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            customer = form.cleaned_data.get("customer_name").user
            staff = form.cleaned_data.get("staff_name").user
            new_form.customer = customer
            new_form.staff = staff
	        
            if form.cleaned_data.get("customer_name").credit_limit == "":
                credit_limit = 0
            else:
                credit_limit = form.cleaned_data.get("customer_name").credit_limit
            new_form.created_by = request.user
            if form.cleaned_data.get("customer_name").credit_limit == '':
                credit_limit = 0
            else:
                credit_limit = form.cleaned_data.get(
                    "customer_name").credit_limit
            user_branch_obj = UserProfile.objects.filter(
                user=request.user).first().branch
            new_form.sale_branch = user_branch_obj
            try:
                new_form.sale_date = datetime.datetime.strptime(
                    str(request.POST.get("sale_date")).strip(), "%d %B %Y").date()
            except:
                new_form.sale_date = datetime.datetime.strptime(
                    str(request.POST.get("sale_date")).strip(), "%d %B, %Y").date()
            total_sale_dept = get_customer_debt(
                customer.pk) + float(request.POST.get("total_price"))
            if total_sale_dept > float(credit_limit)  and not form.cleaned_data.get("sale_type"):
                new_form.waiting_approval = True

            products = request.POST.getlist("product_selected")
            quantities = request.POST.getlist("quantity_selected")
            prices = request.POST.getlist("price_selected")
            print(products)
            print(quantities)
            print(prices)
            if total_sale_dept > float(form.cleaned_data.get("customer_name").credit_limit) and not form.cleaned_data.get("sale_type"):
                new_form.save()

                for (product, quantity, price) in zip(products, quantities, prices):
                    saleItem = SaleItem()
                    saleItem.sale = new_form
                    saleItem.product = Product.objects.filter(
                        id=product).first()
                    saleItem.quantity = quantity
                    saleItem.price = price
                    saleItem.save()
                info = {
                    "status": True,
                    "message": "Successfully Registered and Waiting Approval",
                    "id": new_form.pk
                }
                context.append(info)
                return HttpResponse(json.dumps(context))
            else:
                new_form.save()
                if form.cleaned_data.get("payment_method"):
                    if not form.cleaned_data.get("payment_method") == "Cash Collections":
                        account_transaction = AccountTransaction()
                        account_transaction.account = Account.objects.filter(
                            id=form.cleaned_data.get("payment_method")).first()
                        account_transaction.amount = request.POST.get(
                            "total_price")
                        account_transaction.transanction_type = "deposit"
                        account_transaction.created_by = request.user
                        account_transaction.content_object = new_form
                        account_transaction.save()
                for (product, quantity, price) in zip(products, quantities, prices):
                    saleItem = SaleItem()
                    saleItem.sale = new_form
                    saleItem.product = Product.objects.filter(id=product).first()
                    saleItem.quantity = quantity
                    saleItem.price = price
                    saleItem.save()
                info = {
                    "status": True,
                    "message": "Successfully Registered",
                    "id": new_form.pk
                }
                context.append(info)
                return HttpResponse(json.dumps(context))

        else:
            print(form.errors)
            context = {
                'title': "Add Sales",
                "form": form
            }
        return render(request, 'pages/add_sales.html', context)


class ApproveSaleView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ApproveSaleView, self).dispatch(request, *args, **kwargs)

    def get(self, request, sale_id):
        context = list()
        if Sale.objects.filter(id=sale_id).filter(waiting_approval=True).exists():
            sale = Sale.objects.get(id=sale_id)
            sale.waiting_approval = False
            sale.approved_by = request.user
            sale.save()
            if not Sale.objects.filter(id=sale_id).filter(waiting_approval=True).exists():
                info = {
                    'status': True,
                    'message': "Sale approved"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to approve sale"
                }
        else:
            info = {
                'status': False,
                'message': "Sale with this id not found"
            }
        context.append(info)
        return HttpResponse(json.dumps(context))


class ProductView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        products = Product.objects.all().order_by('name')
        form = ProductForm()
        context = {
            'title': "Products",
            'products': products,
            'form': form,
        }
        return render(request, "pages/products.html", context)

    def post(self, request):
        context = list()
        form = ProductForm(False, request.POST)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Product added successfully"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "pages/products.html", {'form': form, 'products': Product.objects.all()})


class EditProductView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request, product_id):
        products = Product.objects.all().order_by("name")
        product = Product.objects.filter(id=product_id).first()
        form = ProductForm(instance=product)
        context = {
            'title': "Edit Product",
            'form': form,
            'product': product,
            'products': products,
        }
        return render(request, "common/edit_product.html", context)

    def post(self, request, product_id):
        context = list()
        product = Product.objects.filter(id=product_id).first()
        form = ProductForm(True, request.POST, instance=product)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Product edited.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/edit_product.html",
                          {'form': form, 'products': Product.objects.all(), 'title': "Edit Product"})


@never_cache
@login_required(login_url="/auth/login/")
def delete_product(request, product_id):
    context = list()
    if Product.objects.filter(id=product_id):
        Product.objects.filter(id=product_id).delete()
        if not Product.objects.filter(id=product_id).exists():
            info = {
                'status': True,
                'message': "Product succesfully deleted"
            }
        else:
            info = {
                'status': False,
                'message': "Failed to delete Product"
            }
    else:
        info = {
            'status': False,
            'message': "Product does not exists"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login/")
def block_product(request, product_id):
    context = list()
    if Product.objects.filter(id=product_id).filter(is_active=True):
        Product.objects.filter(id=product_id).update(is_active=False)
        if not Product.objects.filter(id=product_id).filter(is_active=True).exists():
            info = {
                'status': True,
                'message': "Product blocked"
            }
        else:
            info = {
                'status': False,
                'message': "Failed to block Product"
            }
    else:
        info = {
            'status': False,
            'message': "Product does not exists"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login/")
def unblock_product(request, product_id):
    context = list()
    if Product.objects.filter(id=product_id).filter(is_active=False):
        Product.objects.filter(id=product_id).update(is_active=True)
        if not Product.objects.filter(id=product_id).filter(is_active=False).exists():
            info = {
                'status': True,
                'message': "Product blocked"
            }
        else:
            info = {
                'status': False,
                'message': "Failed to block Product"
            }
    else:
        info = {
            'status': False,
            'message': "Product does not exists"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


class ExpenseView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required(login_url='/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ExpenseView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = ExpenseForm()
        expenses = Expense.objects.filter(
            expense_date=datetime.datetime.now().date()).order_by("-id")
        context = {
            'title': "Expenses",
            "form": form,
            "expenses": expenses,
        }
        return render(request, 'pages/expenses.html', context)

    def post(self, request, *args, **kwargs):
        context = list()
        form = ExpenseForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            try:
                new_form.expense_date = datetime.datetime.strptime(
                    str(request.POST.get("expense_date")).strip(), "%d %B %Y").date()
            except:
                new_form.expense_date = datetime.datetime.strptime(
                    str(request.POST.get("expense_date")).strip(), "%d %B, %Y").date()
            new_form.save()

            for detail, expense_amount in zip(request.POST.getlist("detail"), request.POST.getlist("expense_amount")):
                expense_item_obj = ExpenseDetail()
                expense_item_obj.detail = detail
                expense_item_obj.expense_amount = expense_amount
                expense_item_obj.expense = new_form
                expense_item_obj.save()
            if form.cleaned_data.get("payment_method"):
                if not form.cleaned_data.get("payment_method") == "Cash Collections":
                    account_transaction = AccountTransaction()
                    account_transaction.account = Account.objects.filter(
                        id=form.cleaned_data.get("payment_method")).first()
                    account_transaction.amount = get_total_expense_detail(
                        new_form.pk)
                    account_transaction.transanction_type = "withdraw"
                    account_transaction.created_by = request.user
                    account_transaction.content_object = new_form
                    account_transaction.save()
            info = {
                "status": True,
                "message": "Successfully Registered"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            print(form.errors)
            info = {
                "status": False,
                "message": "Failed To Register"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login/")
def expense_detail_list(request, *args, **kwargs):
    expense_obj = Expense.objects.filter(id=kwargs.get("pk")).first()
    expense_details = ExpenseDetail.objects.filter(expense=expense_obj)
    context = {
        "expense_details": expense_details
    }
    return render(request, "common/expense_detail_list.html", context)


@never_cache
@login_required(login_url="/auth/login/")
def delete_expense_item(request, *args, **kwargs):
    try:
        context = list()
        Expense.objects.filter(id=kwargs.get("pk")).delete()
        info = {
            "status": True,
            "message": "Successfuly Removed"
        }
        context.append(info)
        return HttpResponse(json.dumps(context))
    except:
        context = list()
        info = {
            "status": False,
            "message": "Failed To Remove"
        }
        return HttpResponse(json.dumps(context))


class AddPurchaseItemView(View):
    def get(self, request, *args, **kwargs):
        form = PurchaseItemForm()
        purchase_obj = Purchase.objects.filter(id=kwargs.get("pk")).first()
        purchases = PurchaseItem.objects.filter(purchase=purchase_obj)
        context = {
            'title': "Purchases Item",
            "form": form,
            "purchases": purchases,
            "purchase_obj": purchase_obj
        }
        return render(request, "common/add_purchase_item.html", context)

    def post(self, request, *args, **kwargs):
        context = list()
        purchase_obj = Purchase.objects.filter(id=kwargs.get("pk")).first()
        form = PurchaseItemForm(request.POST)
        if form.is_valid():
            print('am in')
            new_form = form.save(commit=False)
            new_form.purchase = purchase_obj
            new_form.save()
            info = {
                "status": True,
                "message": "Successfuly Registered"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            print('---------purchase-------')
            print(form.errors)
            print('---------end purchase-------')
            context = {
                'title': "Purchases",
                "form": form,
                "purchase_obj": purchase_obj
            }
            return render(request, 'pages/add_purchase_item.html', context)


class AddPurchaseView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddPurchaseView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        last_purchase = Purchase.objects.filter(
            created_by=request.user).filter(id=kwargs.get("pk")).last()
        form = PurchaseForm(instance=last_purchase)
        context = {
            "form": form,
            "last_purchase": last_purchase
        }
        return render(request, "common/add_purchase.html", context)

    def post(self, request, *args, **kwargs):
        context = list()
        form = PurchaseForm(None, request.POST)
        userProfile_obj = UserProfile.objects.filter(user=request.user).first()
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.supplier = form.cleaned_data.get("supplier_name").user
            new_form.created_by = request.user
            try:
                new_form.purchase_date = datetime.datetime.strptime(
                    str(request.POST.get("purchase_date")).strip(), "%d %B %Y").date()
            except:
                new_form.purchase_date = datetime.datetime.strptime(
                    str(request.POST.get("purchase_date")).strip(), "%d %B, %Y").date()
            new_form.purchase_branch = userProfile_obj.branch
            new_form.save()
            if form.cleaned_data.get("payment_method"):
                if not form.cleaned_data.get("payment_method") == "Cash Collections":
                    account_transaction = AccountTransaction()
                    account_transaction.account = Account.objects.filter(
                        id=form.cleaned_data.get("payment_method")).first()
                    account_transaction.amount = get_total_expense_detail(
                        new_form.pk)
                    account_transaction.transanction_type = "withdraw"
                    account_transaction.created_by = request.user
                    account_transaction.content_object = new_form
                    account_transaction.save()
            last_purchase = Purchase.objects.filter(
                created_by=request.user).last()
            info = {
                "status": True,
                "last": last_purchase.pk if last_purchase else None if request.POST.get("last") == "1" else None,
                "message": "Successfuly Registered"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            print(form.errors)
            context = {
                "form": form
            }
            return render(request, "common/add_purchase.html", context)


class PurchasesView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required(login_url='/auth/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if kwargs.get("pk"):
            last_purchase = Purchase.objects.filter(
                created_by=request.user).filter(id=kwargs.get("pk")).last()
            if last_purchase.supplier:
                form = PurchaseForm(
                    last_purchase.supplier.pk, instance=last_purchase)
            else:
                form = PurchaseForm(None)
        else:
            form = PurchaseForm(None)
        purchases = Purchase.objects.filter(is_active=True).order_by('-id')
        context = {
            'title': "Purchases",
            "form": form,
            "purchases": purchases
        }
        return render(request, 'pages/purchases.html', context)


@never_cache
@login_required(login_url="/auth/login/")
def delete_purchase_item(request, *args, **kwargs):
    try:
        context = list()
        Purchase.objects.filter(id=kwargs.get("pk")).delete()
        info = {
            "status": True,
            "message": "Successfuly Removed"
        }
        context.append(info)
        return HttpResponse(json.dumps(context))
    except:
        context = list()
        info = {
            "status": False,
            "message": "Failed To Remove"
        }
        return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login/")
def delete_purchase(request, *args, **kwargs):
    try:
        context = list()
        Purchase.objects.filter(id=kwargs.get("pk")).delete()
        info = {
            "status": True,
            "message": "Successfuly Removed"
        }
        context.append(info)
        return HttpResponse(json.dumps(context))
    except:
        context = list()
        info = {
            "status": False,
            "message": "Failed To Remove"
        }
        return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login/")
def product_short_name(request, *args, **kwargs):
    context = list()
    product_obj = Product.objects.filter(id=kwargs.get("pk")).first()
    info = {
        "status": True,
        "unit": product_obj.unit
    }
    context.append(info)
    return HttpResponse(json.dumps(context))


class StockView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StockView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        products = Product.objects.all().order_by("name")
        context = {
            'title': "Stocks",
            "products": products,
        }
        return render(request, 'pages/stocks.html', context)


class PaymentView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        customer_payment_form = CustomerPaymentForm()
        context = {
            'title': "Payments",
            'customer_payment_form': customer_payment_form,
            'staff_collection_form': StaffCollectionForm(),
            'loan_collection_form': LoanCollectionForm(),
            'supplier_payment_form': SupplierPaymentForm(),
            'other_payment_form': OtherPaymentForm(),
            'loan_provision_form': LoanProvisionForm(),
            'staff_loan_form': StaffLoanForm(),
        }
        return render(request, 'pages/payments.html', context)


class CustomerPaymentView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CustomerPaymentView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = CustomerPaymentForm(request.POST)
        if form.is_valid():
            try:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B %Y").date()
            except:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B, %Y").date()
            payment = Payment()
            payment.user = form.cleaned_data.get("customer").user
            payment.payment_type = "customer payment"
            payment.amount = form.cleaned_data.get("amount")
            payment.collected_by = form.cleaned_data.get("collected_by").user
            payment.payment_branch = form.cleaned_data.get(
                "collected_by").branch
            payment.description = form.cleaned_data.get("description")
            payment.payment_date = payment_date
            payment.created_by = request.user
            payment.save()
            payment.refresh_from_db()
            if form.cleaned_data.get("payment_method"):
                if not form.cleaned_data.get("payment_method") == "Cash Collections":
                    print(form.cleaned_data.get("payment_method"))
                    account_transaction = AccountTransaction()
                    account_transaction.account = Account.objects.filter(
                        id=form.cleaned_data.get("payment_method")).first()
                    account_transaction.amount = form.cleaned_data.get(
                        "amount")
                    account_transaction.transanction_type = "deposit"
                    account_transaction.created_by = request.user
                    account_transaction.content_object = payment
                    account_transaction.save()

            info = {
                'status': True,
                'message': "Payment registered and saved.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/customer_payment_form.html", {'customer_payment_form': form})


class StaffCollectionView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffCollectionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = StaffCollectionForm(request.POST)
        if form.is_valid():
            try:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B %Y").date()
            except:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B, %Y").date()
            payment = Payment()
            payment.user = form.cleaned_data.get("staff").user
            payment.payment_type = "staff collection"
            payment.amount = form.cleaned_data.get("amount")
            payment.collected_by = form.cleaned_data.get("collected_by").user
            payment.description = form.cleaned_data.get("description")
            payment.payment_date = payment_date
            payment.created_by = request.user
            payment.save()

            info = {
                'status': True,
                'message': "Payment registered and saved.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/staff_collection_form.html", {'staff_collection_form': form})


class LoanCollectionView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoanCollectionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = LoanCollectionForm(request.POST)
        if form.is_valid():
            payment = Payment()
            payment.user = form.cleaned_data.get("borrower").user
            payment.payment_type = "loan collection"
            payment.amount = form.cleaned_data.get("amount")
            payment.collected_by = form.cleaned_data.get("collected_by").user
            payment.payment_branch = form.cleaned_data.get(
                "collected_by").branch
            payment.authorized_by = form.cleaned_data.get("authorized_by").user
            payment.description = form.cleaned_data.get("description")
            payment.created_by = request.user
            payment.save()
            payment.refresh_from_db()
            if form.cleaned_data.get("payment_method"):
                if not form.cleaned_data.get("payment_method") == "Cash Collections":
                    account_transaction = AccountTransaction()
                    account_transaction.account = Account.objects.filter(
                        id=form.cleaned_data.get("payment_method")).first()
                    account_transaction.amount = form.cleaned_data.get(
                        "amount")
                    account_transaction.transanction_type = "deposit"
                    account_transaction.created_by = request.user
                    account_transaction.content_object = payment
                    account_transaction.save()

            info = {
                'status': True,
                'message': "Payment registered and saved.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/loan_collection_form.html", {'loan_collection_form': form})


class SupplierPaymentView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SupplierPaymentView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = SupplierPaymentForm(request.POST)
        if form.is_valid():
            try:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B %Y").date()
            except:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B, %Y").date()
            payment = Payment()
            payment.user = form.cleaned_data.get("supplier").user
            payment.payment_type = "supplier payment"
            payment.amount = form.cleaned_data.get("amount")
            payment.description = form.cleaned_data.get("description")
            payment.created_by = request.user
            payment.payment_branch = UserProfile.objects.filter(
                user=request.user).first().branch
            payment.payment_date = payment_date
            payment.save()
            payment.refresh_from_db()
            if form.cleaned_data.get("payment_method"):
                if not form.cleaned_data.get("payment_method") == "Cash Collections":
                    account_transaction = AccountTransaction()
                    account_transaction.account = Account.objects.filter(
                        id=form.cleaned_data.get("payment_method")).first()
                    account_transaction.amount = form.cleaned_data.get(
                        "amount")
                    account_transaction.transanction_type = "withdraw"
                    account_transaction.created_by = request.user
                    account_transaction.content_object = payment
                    account_transaction.save()

            info = {
                'status': True,
                'message': "Payment registered and saved.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/supplier_payment_form.html", {'supplier_payment_form': form})


class OtherPaymentView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(OtherPaymentView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = OtherPaymentForm(request.POST)
        if form.is_valid():
            try:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B %Y").date()
            except:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B, %Y").date()
            payment = Payment()
            payment.payment_type = "other payment"
            payment.amount = form.cleaned_data.get("amount")
            payment.description = form.cleaned_data.get("description")
            payment.created_by = request.user
            payment.payment_branch = UserProfile.objects.filter(
                user=request.user).first().branch
            payment.payment_date = payment_date
            payment.save()
            payment.refresh_from_db()
            if form.cleaned_data.get("payment_method"):
                if not form.cleaned_data.get("payment_method") == "Cash Collections":
                    account_transaction = AccountTransaction()
                    account_transaction.account = Account.objects.filter(
                        id=form.cleaned_data.get("payment_method")).first()
                    account_transaction.amount = form.cleaned_data.get(
                        "amount")
                    account_transaction.transanction_type = "withdraw"
                    account_transaction.created_by = request.user
                    account_transaction.content_object = payment
                    account_transaction.save()

            info = {
                'status': True,
                'message': "Payment registered and saved.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/other_payment_form.html", {'other_payment_form': form})


class LoanProvisionView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoanProvisionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = LoanProvisionForm(request.POST)
        if form.is_valid():
            try:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B %Y").date()
            except:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B, %Y").date()
            payment = Payment()
            payment.user = form.cleaned_data.get("borrower").user
            payment.payment_type = "loan provision"
            payment.amount = form.cleaned_data.get("amount")
            payment.collected_by = form.cleaned_data.get("collected_by").user
            payment.authorized_by = form.cleaned_data.get("authorized_by").user
            payment.description = form.cleaned_data.get("description")
            payment.created_by = request.user
            payment.payment_branch = UserProfile.objects.filter(
                user=request.user).first().branch
            payment.payment_date = payment_date
            payment.save()
            payment.refresh_from_db()

            if form.cleaned_data.get("payment_method"):
                if not form.cleaned_data.get("payment_method") == "Cash Collections":
                    account_transaction = AccountTransaction()
                    account_transaction.account = Account.objects.filter(
                        id=form.cleaned_data.get("payment_method")).first()
                    account_transaction.amount = form.cleaned_data.get(
                        "amount")
                    account_transaction.transanction_type = "withdraw"
                    account_transaction.created_by = request.user
                    account_transaction.content_object = payment
                    account_transaction.save()

            info = {
                'status': True,
                'message': "Payment registered and saved.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/loan_provision_form.html", {'loan_provision_form': form})


class StaffLoanView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffLoanView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = StaffLoanForm(request.POST)
        if form.is_valid():
            try:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B %Y").date()
            except:
                payment_date = datetime.datetime.strptime(
                    str(request.POST.get("payment_date")).strip(), "%d %B, %Y").date()
            payment = Payment()
            payment.user = form.cleaned_data.get("staff").user
            payment.payment_type = "staff loan"
            payment.amount = form.cleaned_data.get("amount")
            payment.deduction_amount = form.cleaned_data.get(
                "deduction_amount")
            payment.collected_by = form.cleaned_data.get("collected_by").user
            payment.authorized_by = form.cleaned_data.get("authorized_by").user
            payment.description = form.cleaned_data.get("description")
            payment.created_by = request.user
            payment.payment_branch = UserProfile.objects.filter(
                user=request.user).first().branch
            payment.payment_date = payment_date
            payment.save()
            payment.refresh_from_db()
            if form.cleaned_data.get("payment_method"):
                if not form.cleaned_data.get("payment_method") == "Cash Collections":
                    account_transaction = AccountTransaction()
                    account_transaction.account = Account.objects.filter(
                        id=form.cleaned_data.get("payment_method")).first()
                    account_transaction.amount = form.cleaned_data.get(
                        "amount")
                    account_transaction.transanction_type = "withdraw"
                    account_transaction.created_by = request.user
                    account_transaction.content_object = payment
                    account_transaction.save()

            info = {
                'status': True,
                'message': "Payment registered and saved.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            print(form.errors)
            return render(request, "common/staff_loan_form.html", {'staff_loan_form': form})


class RORView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RORView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = RORForm()
        ror_objs = ROR.objects.all().order_by('-id')
        context = {
            'title': 'ROR Calculator',
            'form': form,
            'ror_objs': ror_objs,
        }
        return render(request, 'pages/ror.html', context)

    def post(self, request):
        context = list()
        form = RORForm(request.POST)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': 'ROR Record succesful saved.'
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            print(form.errors)
            return render(request, 'pages/ror.html', {'form': form})


class EditRORView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditRORView, self).dispatch(request, *args, **kwargs)

    def get(self, request, ror_id):
        ror_objs = ROR.objects.all().order_by('-id')
        ror = ROR.objects.filter(id=ror_id).first()
        form = RORForm(instance=ror)
        context = {
            'title': 'Edit ROR Commodity',
            'form': form,
            'ror_objs': ror_objs,
            'ror': ror
        }
        return render(request, 'pages/edit_ror.html', context)

    def post(self, request, ror_id):
        context = list()
        ror_objs = ROR.objects.all().order_by('-id')
        ror = ROR.objects.filter(id=ror_id).first()
        form = RORForm(request.POST, instance=ror)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "ROR edited.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "pages/edit_ror.html",
                          {'form': form, 'ror_obj': ror_objs, 'title': "ROR Product"})


@never_cache
@login_required(login_url="/auth/login/")
def delete_ror_commodity(request, ror_id):
    context = list()
    if ROR.objects.filter(id=ror_id):
        ROR.objects.filter(id=ror_id).delete()
        if not ROR.objects.filter(id=ror_id).exists():
            info = {
                'status': True,
                'message': "ROR Commodity succesfully deleted"
            }
        else:
            info = {
                'status': False,
                'message': "Failed to ROR Commodity"
            }
    else:
        info = {
            'status': False,
            'message': "ROR Commodity does not exists"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))
