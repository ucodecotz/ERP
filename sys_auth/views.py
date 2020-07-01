from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from home.models import Expense, ExpenseDetail
from .models import *
from .forms import *
from django.http import HttpResponse
import json
import random
import string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.conf import settings
from control.models import UserProfile, UserType
import datetime
from control.models import UserProfile
from home.models import Sale, SaleItem, Payment, Purchase


class UsersView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UsersView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        title = "Users"
        customers = UserProfile.objects.filter(user_type="Customer").filter(
            user__is_superuser=False).order_by("user__first_name")
        suppliers = UserProfile.objects.filter(user_type="Supplier").filter(
            user__is_superuser=False).order_by("user__first_name")
        borrowers = UserProfile.objects.filter(user_type="Borrower").filter(
            user__is_superuser=False).order_by("user__first_name")
        staffs = UserProfile.objects.filter(user_type="Staff").filter(
            user__is_superuser=False).order_by("user__first_name")
        context = {
            'title': title,
            'customers': customers,
            'suppliers': suppliers,
            'borrowers': borrowers,
            'total_customers': customers.count(),
            'total_suppliers': suppliers.count(),
            'total_staffs': staffs.count(),
            'total_borrowers': borrowers.count(),
            'staffs': staffs,
            'customer_form': CustomerForm(),
            'supplier_form': SupplierForm(),
            'borrower_form': BorrowerForm(),
            'staff_form': StaffForm(),
        }
        return render(request, "auth/users.html", context)


def createUsername(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


class AddCustomerView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddCustomerView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = CustomerForm(False, request.POST)
        if form.is_valid():
            names = form.cleaned_data.get('full_name').split()
            if not len(names) > 1:
                info = {
                    'status': False,
                    'message': "Full name must contains space between First and Last name"
                }
                context.append(info)
                return HttpResponse(json.dumps(context))
            else:
                first_name = names[0].capitalize()
                last_name = names[1].capitalize()
            user_obj = User()
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.username = createUsername()
            user_obj.email = form.cleaned_data.get('email').lower()
            user_obj.save()
            user_obj.refresh_from_db()

            added_by_obj = form.cleaned_data.get("added_by").user

            try:
                created_date = datetime.datetime.strptime(
                    str(request.POST.get("created_date")).strip(), "%d %B %Y").date()
            except:
                created_date = datetime.datetime.strptime(
                    str(request.POST.get("created_date")).strip(), "%d %B, %Y").date()

            user_profile = UserProfile()
            user_profile.user = user_obj
            user_profile.user_type = "Customer"
            user_profile.phone_number = form.cleaned_data.get('phone_number')
            user_profile.location = form.cleaned_data.get(
                'location').capitalize()
            user_profile.credit_limit = form.cleaned_data.get('credit_limit')
            if form.cleaned_data.get('credit_day'):
                user_profile.credit_day = int(
                    form.cleaned_data.get('credit_day'))
            user_profile.balance = form.cleaned_data.get('balance')
            user_profile.registered_date = created_date
            user_profile.added_by = added_by_obj
            user_profile.save()

            info = {
                'status': True,
                'message': "Successfully registered.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            print(form.errors)
            title = "Users"
            customers = UserProfile.objects.filter(user_type="Customer")
            suppliers = UserProfile.objects.filter(user_type="Supplier")
            borrowers = UserProfile.objects.filter(user_type="Borrower")
            staffs = UserProfile.objects.filter(user_type="Staff")
            context_data = {
                'title': title,
                'customers': customers,
                'suppliers': suppliers,
                'borrowers': borrowers,
                'staffs': staffs,
                'total_customers': customers.count(),
                'total_suppliers': suppliers.count(),
                'total_staffs': staffs.count(),
                'total_borrowers': borrowers.count(),
                'customer_form': form,
                'supplier_form': SupplierForm(),
                'borrower_form': BorrowerForm(),
            }
            return render(request, "auth/users.html", context_data)


class EditCustomerView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditCustomerView, self).dispatch(request, *args, **kwargs)

    def get(self, request, customer_id):
        customer = UserProfile.objects.get(id=customer_id)
        added_by = UserProfile.objects.filter(
            user=User.objects.filter(id=customer.added_by.id).first()).first()
        form = CustomerForm(initial={
            'full_name': customer,
            'email': customer.user.email,
            'phone_number': customer.phone_number,
            'location': customer.location,
            'credit_limit': customer.credit_limit,
            'credit_day': customer.credit_day,
            'added_by': added_by,
            'balance': customer.balance,
        })
        context = {
            'customer_form': form,
            'customer': customer,
        }
        return render(request, "common/edit_customer.html", context)

    def post(self, request, customer_id):
        context = list()
        customer = UserProfile.objects.get(id=customer_id)
        form = CustomerForm(True, request.POST)
        if form.is_valid():
            names = form.cleaned_data.get('full_name').split()
            if not len(names) > 1:
                info = {
                    'status': False,
                    'message': "Full name must contains space between First and Last name"
                }
                context.append(info)
                return HttpResponse(json.dumps(context))
            else:
                first_name = names[0].capitalize()
                last_name = names[1].capitalize()
            user_obj = User()
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj = User.objects.get(id=customer.user.id)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = form.cleaned_data.get("email").lower()
            user_obj.save()

            customer.phone_number = form.cleaned_data.get("phone_number")
            customer.credit_limit = form.cleaned_data.get("credit_limit")
            customer.credit_day = form.cleaned_data.get("credit_day")
            if form.cleaned_data.get("added_by"):
                added_by = form.cleaned_data.get("added_by").user
            else:
                added_by = customer.added_by
            customer.added_by = added_by
            customer.location = form.cleaned_data.get('location').capitalize()
            customer.balance = request.POST.get('balance')
            customer.save()
            info = {
                'status': True,
                'message': "Successfully Edited.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            print(form.errors)
            return render(request, "common/edit_customer.html", {'customer_form': form, 'customer': customer})


@never_cache
@login_required(login_url="/auth/login")
def block_customer(request, customer_id):
    context = list()
    if User.objects.filter(id=customer_id).filter(is_active=True).exists():
        if UserProfile.objects.filter(user__id=customer_id).filter(is_active=True).exists():
            User.objects.filter(id=customer_id).update(is_active=False)
            UserProfile.objects.filter(
                user__id=customer_id).update(is_active=False)
            if not User.objects.filter(id=customer_id).filter(
                is_active=True).exists() and not UserProfile.objects.filter(user__id=customer_id).filter(
                    is_active=True).exists():
                info = {
                    'status': True,
                    'message': "Customer blocked"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to block the customer"
                }
        else:
            info = {
                'status': False,
                'message': "Profile with this customer not available"
            }
    else:
        info = {
            'status': False,
            'message': 'User not available'
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login")
def unblock_customer(request, customer_id):
    context = list()
    if User.objects.filter(id=customer_id).filter(is_active=False).exists():
        if UserProfile.objects.filter(user__id=customer_id).filter(is_active=False).exists():
            User.objects.filter(id=customer_id).update(is_active=True)
            UserProfile.objects.filter(
                user__id=customer_id).update(is_active=True)

            if not User.objects.filter(id=customer_id).filter(
                is_active=False).exists() and not UserProfile.objects.filter(user__id=customer_id).filter(
                    is_active=False).exists():
                info = {
                    'status': True,
                    'message': "Customer unblocked"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to unblock the customer"
                }
        else:
            info = {
                'status': False,
                'message': "Profile with this customer not available"
            }
    else:
        info = {
            'status': False,
            'message': 'User not available'
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login")
def delete_customer(request, customer_id):
    context = list()
    if User.objects.filter(id=customer_id).delete():
        info = {
            'status': True,
            'message': "Customer deleted"
        }
    else:
        info = {
            'status': False,
            'message': "Failed to delete customer"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


class AddSupplierView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddSupplierView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = SupplierForm(False, request.POST)
        if form.is_valid():
            names = request.POST.get('full_name').split()
            if not len(names) > 1:
                info = {
                    'status': False,
                    'message': "Full name must contains space between First and Last name"
                }
                context.append(info)
                return HttpResponse(json.dumps(context))
            else:
                first_name = names[0].capitalize()
                last_name = names[1].capitalize()
            user_obj = User()
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = form.cleaned_data.get("email").lower()
            user_obj.username = createUsername()
            user_obj.save()
            user_obj.refresh_from_db()

            try:
                created_date = datetime.datetime.strptime(
                    str(request.POST.get("created_date")).strip(), "%d %B %Y").date()
            except:
                created_date = datetime.datetime.strptime(
                    str(request.POST.get("created_date")).strip(), "%d %B, %Y").date()

            user_profile = UserProfile()
            user_profile.user = user_obj
            user_profile.user_type = "Supplier"
            user_profile.phone_number = request.POST.get('phone_number')
            user_profile.balance = request.POST.get('balance')
            user_profile.registered_date = created_date
            user_profile.save()

            info = {
                'status': True,
                'message': "Successfully registered.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            info = {
                'status': False,
                'message': str(form.errors)
            }
            context.append(info)
            return HttpResponse(json.dumps(context))


class EditSupplierView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditSupplierView, self).dispatch(request, *args, **kwargs)

    def get(self, request, supplier_id):
        supplier = UserProfile.objects.filter(
            id=supplier_id).filter(user_type="Supplier").first()
        form = SupplierForm(initial={
            'full_name': supplier,
            'email': supplier.user.email,
            'phone_number': supplier.phone_number,
            'location': supplier.location,
            'balance': supplier.balance,
        })
        context = {
            'supplier': supplier,
            'supplier_form': form,
        }
        return render(request, "common/edit_supplier.html", context)

    def post(self, request, supplier_id):
        supplier = UserProfile.objects.get(id=supplier_id)
        form = SupplierForm(True, request.POST)
        context = list()
        if form.is_valid():
            names = form.cleaned_data.get('full_name').split()
            if not len(names) > 1:
                info = {
                    'status': False,
                    'message': "Full name must contains space between First and Last name"
                }
                context.append(info)
                return HttpResponse(json.dumps(context))
            else:
                first_name = names[0].capitalize()
                last_name = names[1].capitalize()
            user_obj = User.objects.get(id=supplier.user.id)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = form.cleaned_data.get("email").lower()
            user_obj.save()

            supplier.phone_number = form.cleaned_data.get("phone_number")
            supplier.location = form.cleaned_data.get("location")
            supplier.balance = request.POST.get('balance')
            supplier.save()
            info = {
                'status': True,
                'message': "Supplier informations edited"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/edit_supplier.html", {'supplier_form': form, 'supplier': supplier})


@never_cache
@login_required(login_url="/auth/login")
def block_supplier(request, supplier_id):
    context = list()
    if User.objects.filter(id=supplier_id).filter(is_active=True).exists():
        if UserProfile.objects.filter(user__id=supplier_id).filter(is_active=True).exists():
            User.objects.filter(id=supplier_id).update(is_active=False)
            UserProfile.objects.filter(
                user__id=supplier_id).update(is_active=False)
            if not User.objects.filter(id=supplier_id).filter(
                is_active=True).exists() and not UserProfile.objects.filter(user__id=supplier_id).filter(
                    is_active=True).exists():
                info = {
                    'status': True,
                    'message': "Supplier blocked"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to block the Supplier"
                }
        else:
            info = {
                'status': False,
                'message': "Profile with this supplier not available"
            }
    else:
        info = {
            'status': False,
            'message': 'User not available'
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login")
def unblock_supplier(request, supplier_id):
    context = list()
    if User.objects.filter(id=supplier_id).filter(is_active=False).exists():
        if UserProfile.objects.filter(user__id=supplier_id).filter(is_active=False).exists():
            User.objects.filter(id=supplier_id).update(is_active=True)
            UserProfile.objects.filter(
                user__id=supplier_id).update(is_active=True)

            if not User.objects.filter(id=supplier_id).filter(
                is_active=False).exists() and not UserProfile.objects.filter(user__id=supplier_id).filter(
                    is_active=False).exists():
                info = {
                    'status': True,
                    'message': "Customer unblocked"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to unblock the customer"
                }
        else:
            info = {
                'status': False,
                'message': "Profile with this customer not available"
            }
    else:
        info = {
            'status': False,
            'message': 'User not available'
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="auth/login")
def delete_supplier(request, supplier_id):
    context = list()
    if User.objects.filter(id=supplier_id).delete():
        info = {
            'status': True,
            'message': "Supplier deleted"
        }
    else:
        info = {
            'status': False,
            'message': "Failed to delete Supplier"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


class AddBorrowerView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddBorrowerView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = BorrowerForm(False, request.POST)
        if form.is_valid():
            names = form.cleaned_data.get('full_name').split()
            if not len(names) > 1:
                info = {
                    'status': False,
                    'message': "Full name must contains space between First and Last name"
                }
                context.append(info)
                return HttpResponse(json.dumps(context))
            else:
                first_name = names[0].capitalize()
                last_name = names[1].capitalize()
            user_obj = User()
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.username = createUsername()
            user_obj.save()
            user_obj.refresh_from_db()

            try:
                created_date = datetime.datetime.strptime(
                    str(request.POST.get("created_date")).strip(), "%d %B %Y").date()
            except:
                created_date = datetime.datetime.strptime(
                    str(request.POST.get("created_date")).strip(), "%d %B, %Y").date()

            user_profile = UserProfile()
            user_profile.user = user_obj
            user_profile.user_type = "Borrower"
            user_profile.phone_number = form.cleaned_data.get('phone_number')
            user_profile.balance = form.cleaned_data.get('balance')
            user_profile.registered_date = created_date
            user_profile.save()

            info = {
                'status': True,
                'message': "Successfully registered.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            title = "Users"
            customers = UserProfile.objects.filter(user_type="Customer")
            suppliers = UserProfile.objects.filter(user_type="Supplier")
            borrowers = UserProfile.objects.filter(user_type="Borrower")
            staffs = UserProfile.objects.filter(user_type="Staff")
            context_data = {
                'title': title,
                'customers': customers,
                'suppliers': suppliers,
                'borrowers': borrowers,
                'staffs': staffs,
                'total_customers': customers.count(),
                'total_suppliers': suppliers.count(),
                'total_staffs': staffs.count(),
                'total_borrowers': borrowers.count(),
                'customer_form': CustomerForm(),
                'supplier_form': SupplierForm(),
                'borrower_form': form,
            }
            return render(request, "auth/users.html", context_data)


class EditBorrowerView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditBorrowerView, self).dispatch(request, *args, **kwargs)

    def get(self, request, borrower_id):
        borrower = UserProfile.objects.filter(
            id=borrower_id).filter(user_type="Borrower").first()
        form = BorrowerForm(initial={
            'full_name': borrower,
            'email': borrower.user.email,
            'phone_number': borrower.phone_number,
            'location': borrower.location,
            'balance': borrower.balance,
        })
        context = {
            'borrower': borrower,
            'borrower_form': form,
        }
        return render(request, "common/edit_borrower.html", context)

    def post(self, request, borrower_id):
        borrower = UserProfile.objects.get(id=borrower_id)
        form = BorrowerForm(True, request.POST)
        context = list()
        if form.is_valid():
            names = form.cleaned_data.get('full_name').split()
            if not len(names) > 1:
                info = {
                    'status': False,
                    'message': "Full name must contains space between First and Last name"
                }
                context.append(info)
                return HttpResponse(json.dumps(context))
            else:
                first_name = names[0].capitalize()
                last_name = names[1].capitalize()
            user_obj = User.objects.get(id=borrower.user.id)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = form.cleaned_data.get("email").lower()
            user_obj.save()

            borrower.phone_number = form.cleaned_data.get("phone_number")
            borrower.location = form.cleaned_data.get("location")
            borrower.balance = request.POST.get('balance')
            borrower.save()
            info = {
                'status': True,
                'message': "Borrower informations edited"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/edit_borrower.html", {'borrower_form': form, 'borrower': borrower})


@never_cache
@login_required(login_url="/auth/login")
def block_borrower(request, borrower_id):
    context = list()
    if User.objects.filter(id=borrower_id).filter(is_active=True).exists():
        if UserProfile.objects.filter(user__id=borrower_id).filter(is_active=True).exists():
            User.objects.filter(id=borrower_id).update(is_active=False)
            UserProfile.objects.filter(
                user__id=borrower_id).update(is_active=False)
            if not User.objects.filter(id=borrower_id).filter(
                is_active=True).exists() and not UserProfile.objects.filter(user__id=borrower_id).filter(
                    is_active=True).exists():
                info = {
                    'status': True,
                    'message': "Borrower blocked"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to block the borrower"
                }
        else:
            info = {
                'status': False,
                'message': "Profile with this borrower not available"
            }
    else:
        info = {
            'status': False,
            'message': 'User not available'
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login")
def unblock_borrower(request, borrower_id):
    context = list()
    if User.objects.filter(id=borrower_id).filter(is_active=False).exists():
        if UserProfile.objects.filter(user__id=borrower_id).filter(is_active=False).exists():
            User.objects.filter(id=borrower_id).update(is_active=True)
            UserProfile.objects.filter(
                user__id=borrower_id).update(is_active=True)

            if not User.objects.filter(id=borrower_id).filter(
                is_active=False).exists() and not UserProfile.objects.filter(user__id=borrower_id).filter(
                    is_active=False).exists():
                info = {
                    'status': True,
                    'message': "Borrower unblocked"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to unblock the borrower"
                }
        else:
            info = {
                'status': False,
                'message': "Profile with this borrower not available"
            }
    else:
        info = {
            'status': False,
            'message': 'User not available'
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login")
def delete_borrower(request, borrower_id):
    context = list()
    if User.objects.filter(id=borrower_id).delete():
        info = {
            'status': True,
            'message': "Borrower deleted"
        }
    else:
        info = {
            'status': False,
            'message': "Failed to delete Borrower"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


class AddStaffView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddStaffView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        form = StaffForm(False, request.POST)
        if form.is_valid():
            names = request.POST.get('full_name').split()
            if not len(names) > 1:
                info = {
                    'status': False,
                    'message': "Full name must contains space between First and Last name"
                }
                context.append(info)
                return HttpResponse(json.dumps(context))
            else:
                first_name = names[0].capitalize()
                last_name = names[1].capitalize()
            user_obj = User()
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            if form.cleaned_data.get('email'):
                user_obj.email = form.cleaned_data.get('email').lower()
                if not User.objects.filter(username=form.cleaned_data.get('email').lower()).exists():
                    user_obj.username = form.cleaned_data.get('email').lower()
                else:
                    info = {
                        'status': False,
                        'message': "User with this Email exists try another email",
                    }
                    context.append(info)
                    return HttpResponse(json.dumps(context))
            elif form.cleaned_data.get('phone_number'):
                if not User.objects.filter(username=form.cleaned_data.get("phone_number")).exists():
                    user_obj.username = form.cleaned_data.get("phone_number")
                else:
                    info = {
                        'status': False,
                        'message': "User with this Phone number exists try another phone number please",
                    }
                    context.append(info)
                    return HttpResponse(json.dumps(context))
            else:
                user_obj.username = str(first_name) + \
                    "@staff." + str(last_name)

            if request.POST.get("role"):
                group_obj = Group.objects.filter(
                    id=request.POST.get("role")).first()

            user_obj.is_staff = True
            user_obj.set_password("halisia10@staff")
            user_obj.save()
            user_obj.refresh_from_db()
            user_obj.groups.add(group_obj)

            if request.POST.get("branch"):
                branch_obj = Branch.objects.filter(
                    id=request.POST.get("branch")).first()

            user_profile = UserProfile()
            user_profile.user = user_obj
            user_profile.salary_amount = request.POST.get("salary")
            user_profile.user_type = "Staff"
            user_profile.branch = branch_obj
            user_profile.phone_number = request.POST.get('phone_number')
            user_profile.balance = request.POST.get('balance')
            user_profile.save()

            info = {
                'status': True,
                'message': "Successfully registered.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            title = "Users"
            customers = UserProfile.objects.filter(user_type="Customer")
            suppliers = UserProfile.objects.filter(user_type="Supplier")
            borrowers = UserProfile.objects.filter(user_type="Borrower")
            staffs = UserProfile.objects.filter(user_type="Staff")
            context_data = {
                'title': title,
                'customers': customers,
                'suppliers': suppliers,
                'borrowers': borrowers,
                'staffs': staffs,
                'total_customers': customers.count(),
                'total_suppliers': suppliers.count(),
                'total_staffs': staffs.count(),
                'total_borrowers': borrowers.count(),
                'customer_form': CustomerForm(),
                'supplier_form': SupplierForm(),
                'borrower_form': BorrowerForm(),
                'staff_form': form,
            }
            return render(request, "auth/users.html", context_data)


class EditStaffView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditStaffView, self).dispatch(request, *args, **kwargs)

    def get(self, request, staff_id):
        staff = UserProfile.objects.filter(
            id=staff_id).filter(user_type="Staff").first()
        if staff.user.groups.all().exists():
            roles = staff.user.groups.all()[0]
        else:
            roles = Group.objects.all()
        form = StaffForm(initial={
            'full_name': staff,
            'email': staff.user.email,
            'phone_number': staff.phone_number,
            'salary': staff.salary_amount,
            'branch': staff.branch,
            'role': roles,
            'balance': staff.balance,
        })
        context = {
            'staff': staff,
            'staff_form': form,
        }
        return render(request, "common/edit_staff.html", context)

    def post(self, request, staff_id):
        staff = UserProfile.objects.get(id=staff_id)
        context = list()
        form = StaffForm(True, request.POST)
        if form.is_valid():
            names = form.cleaned_data.get('full_name').split()
            if not len(names) > 1:
                info = {
                    'status': False,
                    'message': "Full name must contains space between First and Last name"
                }
                context.append(info)
                return HttpResponse(json.dumps(context))
            else:
                first_name = names[0].capitalize()
                last_name = names[1].capitalize()
            user_obj = User.objects.get(id=staff.user.id)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            if form.cleaned_data.get('email'):
                user_obj.email = form.cleaned_data.get('email').lower()
                if not User.objects.filter(username=form.cleaned_data.get('email').lower()).exists():
                    user_obj.username = form.cleaned_data.get('email').lower()
            elif form.cleaned_data.get('phone_number'):
                if not User.objects.filter(username=form.cleaned_data.get("phone_number")).exists():
                    user_obj.username = form.cleaned_data.get("phone_number")
            else:
                user_obj.username = user_obj.username

            user_obj.is_staff = True
            user_obj.save()
            user_obj.refresh_from_db()
            if not form.cleaned_data.get("role") in user_obj.groups.all():
                user_obj.groups.add(form.cleaned_data.get("role"))

            staff.salary_amount = form.cleaned_data.get("salary")
            staff.branch = form.cleaned_data.get("branch")
            staff.phone_number = form.cleaned_data.get('phone_number')
            staff.balance = request.POST.get('balance')
            staff.save()
            info = {
                'status': True,
                'message': "Staff informations edited"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/edit_staff.html", {'staff_form': form, 'staff': staff})


class RecoverStaffPasswordView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RecoverStaffPasswordView, self).dispatch(request, *args, **kwargs)

    def get(self, request, staff_id):
        def get_random_password():
            letters = string.ascii_lowercase
            return "".join(random.choice(letters) for i in range(6))

        password = get_random_password()
        staff_user_obj = User.objects.get(id=staff_id)
        staff_user_obj.set_password(password)
        staff_user_obj.save()
        context = {
            "username": staff_user_obj.username,
            "password": password,
        }
        return render(request, "common/staff_recover_password.html", context)


@never_cache
@login_required(login_url="/auth/login")
def block_staff(request, staff_id):
    context = list()
    if User.objects.filter(id=staff_id).filter(is_active=True).filter(is_staff=True).exists():
        if UserProfile.objects.filter(user__id=staff_id).filter(is_active=True).exists():
            User.objects.filter(id=staff_id).update(
                is_active=False, is_staff=False)
            UserProfile.objects.filter(
                user__id=staff_id).update(is_active=False)
            if not User.objects.filter(id=staff_id).filter(is_active=True).filter(
                is_staff=True).exists() and not UserProfile.objects.filter(user__id=staff_id).filter(
                    is_active=True).exists():
                info = {
                    'status': True,
                    'message': "Staff blocked"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to block the staff"
                }
        else:
            info = {
                'status': False,
                'message': "Profile with this staff not available"
            }
    else:
        info = {
            'status': False,
            'message': 'User not available'
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login")
def unblock_staff(request, staff_id):
    context = list()
    if User.objects.filter(id=staff_id).filter(is_active=False).filter(is_staff=False).exists():
        if UserProfile.objects.filter(user__id=staff_id).filter(is_active=False).exists():
            User.objects.filter(id=staff_id).update(
                is_active=True, is_staff=True)
            UserProfile.objects.filter(
                user__id=staff_id).update(is_active=True)

            if not User.objects.filter(id=staff_id).filter(is_active=False).exists() and not UserProfile.objects.filter(
                    user__id=staff_id).filter(is_active=False).exists():
                info = {
                    'status': True,
                    'message': "Staff unblocked"
                }
            else:
                info = {
                    'status': False,
                    'message': "Failed to unblock the staff"
                }
        else:
            info = {
                'status': False,
                'message': "Profile with this staff not available"
            }
    else:
        info = {
            'status': False,
            'message': 'User not available'
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login")
def delete_staff(request, staff_id):
    context = list()
    if User.objects.filter(id=staff_id).delete():
        info = {
            'status': True,
            'message': "Staff deleted"
        }
    else:
        info = {
            'status': False,
            'message': "Failed to delete staff"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


class LogInForm(View):
    form_class = LogInForm
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'sysname': settings.SYS_NAME, 'title': 'Login'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
        else:
            print(form.errors)

        return render(request, self.template_name, {'form': form, 'sysname': settings.SYS_NAME, 'title': 'Login'})


@login_required(login_url='/auth/login/')
def logout_view(request):
    logout(request)
    return redirect("login")


class BadDebtView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BadDebtView, self).dispatch(request, *args, **kwargs)

    def get(self, request, customer_id):
        customer = UserProfile.objects.filter(id=customer_id).first()
        context = {
            'customer': customer,
            'form': BadDebtForm(customer.user.pk)
        }
        return render(request, 'common/bad_debt.html', context)

    def post(self, request, customer_id):
        customer = UserProfile.objects.filter(id=customer_id).first()
        form = BadDebtForm(customer.user.pk, request.POST)
        context = list()
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.customer = customer
            new_form.save()
            if not form.cleaned_data.get("debt_type") == "Staff":
                expense_obj = Expense()
                expense_obj.expense_for = "Bad Debt"
                expense_obj.expense_type = "normal"
                expense_obj.authorized_by = UserProfile.objects.filter(
                    user=request.user).first()
                expense_obj.expense_branch = UserProfile.objects.filter(
                    user=request.user).first().branch
                expense_obj.save()
                expense_obj.refresh_from_db()

                expense_detail_obj = ExpenseDetail()
                expense_detail_obj.expense = expense_obj
                expense_detail_obj.expense_amount = form.cleaned_data.get(
                    "amount")
                expense_detail_obj.detail = form.cleaned_data.get(
                    "description")
                expense_detail_obj.save()
            info = {
                'status': True,
                'message': "Bad Debt Successfully Saved"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/bad_debt.html", {'form': form, 'customer': customer})


class UserGroupView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserGroupView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        title = "Roles & Permissions"
        groups = Group.objects.all().order_by("name")
        form = UserGroupForm()
        context = {
            'title': title,
            'groups': groups,
            'form': form,
        }
        return render(request, "auth/user_groups.html", context)

    def post(self, request):
        context = list()
        title = "Roles & Permissions"
        groups = Group.objects.all()
        form = UserGroupForm(request.POST)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Group added successfully"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "auth/user_groups.html", {'form': form, 'groups': groups, 'title': title})


class EditUserGroupView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditUserGroupView, self).dispatch(request, *args, **kwargs)

    def get(self, request, group_id):
        title = "Edit Roles & Permissions"
        group = Group.objects.get(id=group_id)
        groups = Group.objects.all()
        form = UserGroupForm(instance=group)
        context = {
            'title': title,
            'groups': groups,
            'form': form,
            'group': group,
        }
        return render(request, "auth/edit_user_group.html", context)

    def post(self, request, group_id):
        context = list()
        title = "Edit Roles & Permissions"
        groups = Group.objects.all()
        group = Group.objects.get(id=group_id)
        form = UserGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Group edited successfully"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "auth/edit_user_group.html",
                          {'form': form, 'groups': groups, 'title': title, 'group': group})


@never_cache
@login_required(login_url="/auth/login")
def delete_group(request, group_id):
    context = list()
    if Group.objects.filter(id=group_id).exists():
        Group.objects.filter(id=group_id).delete()
        if not Group.objects.filter(id=group_id).exists():
            info = {
                'status': True,
                'message': "Group deleted"
            }
        else:
            info = {
                'status': False,
                'message': "Failed to delete"
            }
    else:
        info = {
            'status': False,
            'message': "Group with this id not availbale"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url="/auth/login")
def group_permissions(request, group_id):
    group = Group.objects.get(id=group_id)
    assigned = group.permissions.all()
    not_assigned = Permission.objects.all().exclude(
        id__in=[p.id for p in group.permissions.all()])
    context = {
        "assigned": assigned,
        "not_assigned": not_assigned,
        "group": group,
    }
    return render(request, 'common/group_permissions.html', context)


@never_cache
@login_required(login_url="/auth/login")
def assign_group_permission(request, perm_id, group_id):
    permission = Permission.objects.get(id=perm_id)
    group = Group.objects.get(id=group_id)
    group_id = group.id
    group.permissions.add(permission)
    assigned = group.permissions.all()
    context = {
        "assigned": assigned,
        "group": group,
        "group_id": group_id,
    }
    return render(request, "common/assigned_group_permissions.html", context)


@never_cache
@login_required(login_url="/auth/login")
def remove_group_permission(request, perm_id, group_id):
    permission = Permission.objects.get(id=perm_id)
    group = Group.objects.get(id=group_id)
    group.permissions.remove(permission)
    not_assigned = Permission.objects.all().exclude(
        id__in=[p.id for p in group.permissions.all()])
    context = {
        "not_assigned": not_assigned,
        "group": group,
        "group_id": group.id,
    }
    return render(request, "common/not_assigned_group_permissions.html", context)


@never_cache
@login_required(login_url="/auth/login")
def group_staffs(request, group_id):
    group = Group.objects.get(id=group_id)
    assigned = User.objects.filter(groups__id=group_id).filter(
        is_staff=True).exclude(is_superuser=True)
    not_assigned = User.objects.filter(is_staff=True).exclude(
        id__in=[p.id for p in User.objects.filter(groups__id=group_id).filter(is_staff=True)]).exclude(is_superuser=True)
    context = {
        "assigned": assigned,
        "not_assigned": not_assigned,
        "group": group,
    }
    return render(request, 'common/staff_groups.html', context)


@never_cache
@login_required(login_url="/auth/login")
def assign_staff_group(request, staff_id, group_id):
    staff = User.objects.get(id=staff_id).filter(is_superuser=False)
    group = Group.objects.get(id=group_id)
    group_id = group.id
    staff.groups.add(group)
    assigned = User.objects.filter(groups__id=group_id).filter(
        is_staff=True).exclude(is_superuser=True)
    context = {
        "assigned": assigned,
        "not_assigned": User.objects.filter(is_staff=True).exclude(
            id__in=[p.id for p in User.objects.filter(groups__id=group_id).filter(is_staff=True)]).exclude(is_superuser=True),
        "group": group,
        "group_id": group_id,
    }
    return render(request, "common/assigned_staff_group.html", context)


@never_cache
@login_required(login_url="/auth/login")
def remove_staff_group(request, staff_id, group_id):
    staff = User.objects.get(id=staff_id).filter(is_superuser=False)
    group = Group.objects.get(id=group_id)
    staff.groups.remove(group)
    not_assigned = User.objects.filter(is_staff=True).exclude(
        id__in=[p.id for p in User.objects.filter(groups__id=group_id).filter(is_staff=True)])
    context = {
        "not_assigned": not_assigned,
        "assigned": User.objects.filter(groups__id=group_id).filter(is_staff=True),
        "group": group,
        "group_id": group.id,
    }
    return render(request, "common/not_assigned_staff_group.html", context)


class CustomerDetails(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, customer_id):
        user_list = list()
        customer_sales_credit_amount= 0
        customer_sales_cash_amount= 0
        customer_payment_amount= 0
        user_profile_obj = UserProfile.objects.filter(id=customer_id).first()
        for sale in Sale.objects.filter(customer=user_profile_obj.user).filter(is_active=True).order_by("-id"):
            total_items = []
            for item in SaleItem.objects.filter(sale=sale):
                total = float(item.price) * float(item.quantity)
                total_items.append(total)
            user_list.append({
                "name": sale.customer.first_name + ' ' + sale.customer.last_name,
                "date": sale.sale_date,
                "amount": sum(total_items),
                'sale_type': sale.sale_type,
                "type": 'sale'
            })
            for c in user_list:
                if c['type'] == 'sale' and c['sale_type'] == False :
                    customer_sales_credit_amount += float(c['amount'])
                elif c['type'] == 'sale' and c['sale_type'] == True:
                    customer_sales_cash_amount += float(c['amount'])

        if Payment.objects.filter(user=user_profile_obj.user).first():
            for payment in Payment.objects.filter(user=user_profile_obj.user).order_by("-id"):
                user_list.append({
                "name": payment.user.first_name + ' ' + payment.user.last_name,
                "date": payment.payment_date,
                "amount": payment.amount,
                'sale_type': payment.payment_type,
                "type": 'payment'
            })
            for c in user_list:
                if c['type'] == 'payment' and c['sale_type'] == 'customer payment':
                    customer_payment_amount += float(c['amount'])

        context = {
            'title': 'Customer History',
            "sale_lists": user_list,
            'user': user_profile_obj,
            'customer_sales_credit_amount': customer_sales_credit_amount,
            'customer_sales_cash_amount': customer_sales_cash_amount,
            'customer_payment_amount': customer_payment_amount,
        }
        return render(request, 'auth/customer_details.html', context)

class SupplierDetails(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, supplier_id):
        user_list = list()
        customer_purchase_credit_amount= 0
        customer_purchase_cash_amount= 0
        customer_payment_amount= 0
        user_profile_obj = UserProfile.objects.filter(id=supplier_id).first()
        if Purchase.objects.filter(supplier=user_profile_obj.user).filter(is_active=True).order_by("-id").exists():
            purchase_item = Purchase.objects.filter(supplier=user_profile_obj.user).filter(is_active=True).order_by("-id")
            for p in purchase_item:
                user_list.append({
                "date": p.purchase_date,
                "amount": p.buying_price,
                "item_type": str(p.purchase_type),
                "item": p.product.name,
                'type': 'purchase'
                })
            for c in user_list:
                if c['type'] == 'purchase' and c['item_type'] == 'False' :
                    customer_purchase_credit_amount += float(c['amount'])
                elif c['type'] == 'purchase' and c['item_type'] == 'True':
                    customer_purchase_cash_amount += float(c['amount'])

        if Payment.objects.filter(user=user_profile_obj.user).first():
            for payment in Payment.objects.filter(user=user_profile_obj.user).order_by("-id"):
                user_list.append({
                "date": payment.payment_date.date,
                "amount": payment.amount,
                "item_type": str(payment.payment_type),
                "item": '',
                'type': 'payment'
                })
            
            for c in user_list:
                if c['item_type'] == 'supplier payment':
                    customer_payment_amount += float(c['amount'])
            
        context = {
            'title': 'Supplier History',
            "supplier_lists": user_list,
            'user': user_profile_obj,
            'customer_purchase_credit_amount': customer_purchase_credit_amount,
            'customer_purchase_cash_amount': customer_purchase_cash_amount,
            'customer_payment_amount': customer_payment_amount,
        }
        return render(request, 'auth/supplyer_details.html', context)
    

class BorrowerDetails(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, borrower_id):
        user_list = list()
        borrower_loan_amount= 0
        borrower_payments_amount= 0
        user_profile_obj = UserProfile.objects.filter(id=borrower_id).first()


        if Payment.objects.filter(user=user_profile_obj.user).first():
            for payment in Payment.objects.filter(user=user_profile_obj.user).order_by("-id"):
                user_list.append({
                "date": payment.payment_date.date,
                "amount": payment.amount,
                "item_type": payment.payment_type,
                })
            
            for c in user_list:
                if c['item_type'] == 'loan collection':
                    borrower_payments_amount += float(c['amount'])
                elif c['item_type'] == 'loan provision':
                    borrower_loan_amount += float(c['amount'])
            
        context = {
            'title': 'Borrower History',
            "borrower_lists": user_list,
            'user': user_profile_obj,
            'borrower_payments_amount': borrower_payments_amount,
            "borrower_loan_amount": borrower_loan_amount
        }
        return render(request, 'auth/borrower_details.html', context)