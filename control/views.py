from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import View
from django.db.models import Q, Sum
import json
from control.models import *
from control.forms import *
from control.staff_calculation import get_staff_loan
from control.templatetags.control_filters import get_staff_net_pay
import itertools
import datetime
from home.models import Payment, Sale, SaleItem, Expense, ExpenseDetail


class AssetView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AssetView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        title = "Assets"
        form = AssetForm()
        assets = Asset.objects.all().order_by("name")
        context = {
            'title': title,
            'form': form,
            'assets': assets,
            'total_asset': assets.count(),
        }
        return render(request, "home/assets.html", context)

    def post(self, request):
        context = list()
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Asset added successfully"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            assets = Asset.objects.all()
            return render(request, "home/assets.html",
                          {'form': form, 'assets': assets, 'title': "Assets", 'total_asset': assets.count()})


class EditAssetView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditAssetView, self).dispatch(request, *args, **kwargs)

    def get(self, request, asset_id):
        asset_obj = Asset.objects.filter(id=asset_id).first()
        title = "Assets"
        form = AssetForm(instance=asset_obj)
        assets = Asset.objects.all()
        context = {
            'title': title,
            'form': form,
            'assets': assets,
            'asset': asset_obj,
            'total_asset': assets.count(),
        }
        return render(request, "home/edit_asset.html", context)

    def post(self, request, asset_id):
        context = list()
        asset_obj = Asset.objects.filter(id=asset_id).first()
        form = AssetForm(request.POST, instance=asset_obj)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Asset added successfully"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            assets = Asset.objects.all()
            return render(request, "home/edit_asset.html",
                          {'form': form, 'assets': assets, 'title': "Assets", 'asset': asset_obj,
                           'total_asset': assets.count()})


@never_cache
@login_required(login_url="/auth/login/")
def delete_asset(request, asset_id):
    context = list()
    if Asset.objects.filter(id=asset_id):
        Asset.objects.filter(id=asset_id).delete()
        if not Asset.objects.filter(id=asset_id).exists():
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


class RegionView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RegionView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        regions = Region.objects.all().order_by("name")
        context = {
            'title': 'Regions',
            'regions': regions,
            'form': RegionForm(),
            'total_region': regions.count(),
        }
        return render(request, "home/regions.html", context)

    def post(self, request):
        context = list()
        form = RegionForm(False, request.POST)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Region successfully registered.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            regions = Region.objects.all()
            return render(request, "home/regions.html",
                          {'form': form, 'regions': regions, 'title': "Regions", 'total_region': regions.count()})


class EditRegionView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditRegionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, region_id):
        region = Region.objects.filter(id=region_id).first()
        regions = Region.objects.all().order_by("name")
        form = RegionForm(instance=region)
        context = {
            'title': "Edit Region",
            'form': form,
            'region': region,
            'regions': regions,
            'total_region': regions.count(),
        }
        return render(request, "home/edit_region.html", context)

    def post(self, request, region_id):
        context = list()
        region = Region.objects.filter(id=region_id).first()
        form = RegionForm(True, request.POST, instance=region)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Region edited.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            regions = Region.objects.all()
            return render(request, "home/edit_region.html",
                          {'form': form, 'title': "Edit Region", 'regions': regions, 'region': region,
                           'total_region': regions.count()})


@never_cache
@login_required(login_url="/auth/login/")
def delete_region(request, region_id):
    context = list()
    if Region.objects.filter(id=region_id):
        Region.objects.filter(id=region_id).delete()
        if not Region.objects.filter(id=region_id).exists():
            info = {
                'status': True,
                'message': "Region succesfully deleted"
            }
        else:
            info = {
                'status': False,
                'message': "Failed to delete region"
            }
    else:
        info = {
            'status': False,
            'message': "Region does not exists"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


class UserTypeView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserTypeView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        title = "UserTypes"
        form = UserTypeForm()
        user_types = UserType.objects.all()
        context = {
            'title': title,
            'form': form,
            'user_types': user_types,
            'total_user_type': user_types.count(),
        }
        return render(request, "home/user_types.html", context)

    def post(self, request):
        context = list()
        title = "UserTypes"
        form = UserTypeForm(request.POST)
        user_types = UserType.objects.all()
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "User Type saved successfully.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "home/user_types.html", {'form': form, 'title': title, 'user_types': user_types,
                                                            'total_user_type': user_types.count()})


class EditUserTypeView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditUserTypeView, self).dispatch(request, *args, **kwargs)

    def get(self, request, user_type_id):
        title = "Edit User Type"
        user_types = UserType.objects.all()
        user_type = UserType.objects.filter(id=user_type_id).first()
        form = UserTypeForm(instance=user_type)
        context = {
            'title': title,
            'form': form,
            'user_types': user_types,
            'user_type': user_type,
            'total_user_type': user_types.count(),
        }
        return render(request, "home/edit_user_type.html", context)

    def post(self, request, user_type_id):
        context = list()
        title = "Edit User Type"
        user_types = UserType.objects.all()
        user_type = UserType.objects.filter(id=user_type_id).first()
        form = UserTypeForm(request.POST, instance=user_type)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "User Type saved successfully.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "home/edit_user_type.html",
                          {'form': form, 'title': title, 'user_types': user_types, "user_type": user_type,
                           'total_user_type': user_types.count()})


@never_cache
@login_required(login_url="/auth/login/")
def delete_user_type(request, user_type_id):
    context = list()
    if UserType.objects.filter(id=user_type_id).exists():
        UserType.objects.filter(id=user_type_id).delete()
        if not UserType.objects.filter(id=user_type_id).exists():
            info = {
                'status': True,
                'message': "User type deleted successfully"
            }
        else:
            info = {
                'status': False,
                'message': "user type not deleted.."
            }
    else:
        info = {
            'status': False,
            'message': "User Type not exists.."
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


class BranchView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BranchView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        branches = Branch.objects.all().order_by("name")
        title = "Branches"
        form = BranchForm()
        context = {
            'title': title,
            'branches': branches,
            'total_branch': branches.count(),
            'form': form,
        }
        return render(request, "home/branches.html", context)

    def post(self, request):
        context = list()
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Branch successfully added.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            branches = Branch.objects.all()
            return render(request, "home/branches.html",
                          {'form': form, 'title': "Branches", 'branches': branches, 'total_branch': branches.count()})


class EditBranchView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditBranchView, self).dispatch(request, *args, **kwargs)

    def get(self, request, branch_id):
        branch = Branch.objects.filter(id=branch_id).first()
        form = BranchForm(instance=branch)
        branches = Branch.objects.all().order_by("name")
        context = {
            'title': "Edit Branch",
            'form': form,
            'branch': branch,
            'branches': branches,
            'total_branch': branches.count(),
        }
        return render(request, "home/edit_branch.html", context)

    def post(self, request, branch_id):
        context = list()
        branch = Branch.objects.filter(id=branch_id).first()
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Branch edited.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            branches = Branch.objects.all()
            return render(request, "home/edit_branch.html",
                          {'form': form, 'branches': branches, 'title': "Edit Branch", 'branch': branch,
                           'total_branches': branches.count()})


@never_cache
@login_required(login_url="/auth/login/")
def delete_branch(request, branch_id):
    context = list()
    if Branch.objects.filter(id=branch_id):
        Branch.objects.filter(id=branch_id).delete()
        if not Branch.objects.filter(id=branch_id).exists():
            info = {
                'status': True,
                'message': "Branch Successfully deleted"
            }
        else:
            info = {
                'status': False,
                'message': "Failed to delete branch"
            }
    else:
        info = {
            'status': False,
            'message': "Branch does not exists"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


@never_cache
@login_required(login_url='/auth/login/')
def userprofile(request):
    profile = UserProfile.objects.get(user=request.user)
    context = {
        'title': "User Profile",
        'profile': profile,
        'salaries': Salary.objects.filter(staff=profile.user)
    }
    return render(request, 'home/user_profile.html', context)


class UpdateProfileInfoView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateProfileInfoView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        user_obj = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.get(user=user_obj)
        if request.POST.get("phone_number"):
            phone_number = request.POST.get("phone_number")
        if request.POST.get("full_name"):
            names = request.POST.get('full_name').split()
            first_name = names[0].capitalize()
            last_name = names[1].capitalize()
        # if request.POST.get("password") and str(request.POST.get("passowrd")) == str(request.POST.get("confirm_password")):
        #     password = request.POST.get("password")

        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.save()

        profile.phone_number = phone_number
        profile.save()
        info = {
            'status': True,
            'message': "Profile updated successfully"
        }
        context.append(info)
        return HttpResponse(json.dumps(context))


class ChangePasswordView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ChangePasswordView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = list()
        user_obj = User.objects.get(id=request.user.id)
        if request.POST.get("password") and str(request.POST.get("password")) == str(
                request.POST.get("confirm_password")):
            password = request.POST.get("password")
            user_obj.set_password(password)
            user_obj.save()
            logout(request)
            info = {
                'status': True,
                'message': "Password updated"
            }
        else:
            info = {
                'status': False,
                'message': "Password does not match"
            }
        context.append(info)
        return HttpResponse(json.dumps(context))


class Payroll(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Payroll, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        if request.GET.get("month"):
            month = request.GET.get("month")
        if request.GET.get("year"):
            year = request.GET.get("year")
        if int(year) == datetime.datetime.now().year:
            if int(month) <= datetime.datetime.now().month:
                staffs = UserProfile.objects.filter(user__is_active=True).filter(user__is_superuser=False).filter(registered_date__year__lte=year).filter(user_type='Staff').order_by(
                    "-id")
            else:
                staffs = None
        elif int(year) < datetime.datetime.now().year:
            staffs = UserProfile.objects.filter(user__is_active=True).filter(user__is_superuser=False).filter(Q(registered_date__year=year) & Q(registered_date__month__lte=month)).filter(registered_date__year__lte=year).filter(user_type='Staff').order_by(
                "-id")
        else:
            staffs = None
        context = {
            'title': 'Payroll',
            "staffs": staffs,
            "month": month,
            "year": year
        }
        return render(request, 'home/payroll.html', context)


class AccountsView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AccountsView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        from control.account_calculations import get_today_total_cash_amount, get_today_total_bank_amount, \
            get_total_cash_on_hand, get_all_accounts_amount_up_to_date
        title = "Accounts"
        print(get_all_accounts_amount_up_to_date())
        accounts = Account.objects.all().order_by("name")
        total_collection_amount = get_total_cash_on_hand() + get_all_accounts_amount_up_to_date()
        context = {
            'title': title,
            'accounts': accounts,
            'total_accounts': accounts.count(),
            'total_cash_on_hand': get_total_cash_on_hand(),
            'total_collection_amount': total_collection_amount,
        }
        return render(request, "home/all_accounts.html", context)


class AddAccountView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddAccountView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = AccountForm()
        context = {
            'form': form,
        }
        return render(request, "common/add_account_form.html", context)

    def post(self, request):
        context = list()
        form = AccountForm(False, request.POST)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Account registered successfully.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/add_account_form.html", {'form': form})


class EditAccountView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditAccountView, self).dispatch(request, *args, **kwargs)

    def get(self, request, account_id):
        account = Account.objects.get(id=account_id)
        form = AccountForm(instance=account)
        context = {
            'form': form,
            'account': account,
        }
        return render(request, "common/edit_account_form.html", context)

    def post(self, request, account_id):
        account = Account.objects.get(id=account_id)
        context = list()
        form = AccountForm(True, request.POST, instance=account)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Account registered successfully.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/edit_account_form.html", {'form': form, 'account': account})


@never_cache
@login_required(login_url="/auth/login")
def delete_account(request, account_id):
    context = list()
    if Account.objects.filter(id=account_id).exists():
        Account.objects.filter(id=account_id).delete()
        if not Account.objects.filter(id=account_id).exists():
            info = {
                'status': True,
                'message': "Account deleted"
            }
        else:
            info = {
                'status': False,
                'message': "Failed to delete account"
            }
    else:
        info = {
            'status': False,
            'message': "Account with this id does not exists"
        }
    context.append(info)
    return HttpResponse(json.dumps(context))


class AccountTransactionsView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AccountTransactionsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, account_id):
        account = Account.objects.get(id=account_id)
        transactions = AccountTransaction.objects.filter(account=account)
        total_deposit = \
            AccountTransaction.objects.filter(account=account).filter(transanction_type="deposit").aggregate(
                Sum('amount'))[
                "amount__sum"]
        total_withdraw = \
            AccountTransaction.objects.filter(account=account).filter(transanction_type="withdraw").aggregate(
                Sum('amount'))[
                "amount__sum"]

        total_transfer = \
            AccountTransaction.objects.filter(account=account).filter(transanction_type="transfer").aggregate(
                Sum('amount'))[
                "amount__sum"]
        if total_deposit:
            total_deposit = total_deposit
        else:
            total_deposit = 0
        if total_withdraw:
            total_withdraw = total_withdraw
        else:
            total_withdraw = 0
        if total_transfer:
            total_transfer = total_transfer
        else:
            total_transfer = 0
        title = "Account Transactions"
        context = {
            'title': title,
            'account': account,
            'transactions': transactions,
            'total_deposit': total_deposit,
            'total_withdraw': total_withdraw,
            'total_transfer': total_transfer
        }
        return render(request, "home/account_transactions.html", context)


class AccountDepositView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AccountDepositView, self).dispatch(request, *args, **kwargs)

    def get(self, request, account_id):
        account = Account.objects.get(id=account_id)
        form = AccountTransanctionForm(initial={
            'transanction_type': "deposit"
        })
        context = {
            'form': form,
            'account': account,
        }
        return render(request, "common/account_deposit.html", context)

    def post(self, request, account_id):
        account = Account.objects.get(id=account_id)
        context = list()
        form = AccountTransanctionForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.account = Account.objects.get(id=account_id)
            new_form.created_by = request.user
            new_form.transanction_type = "deposit"
            new_form.save()
            info = {
                'status': True,
                'message': "Fund deposited successfully.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/account_deposit.html", {'form': form, 'account': account})


class AccountTransferView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AccountTransferView, self).dispatch(request, *args, **kwargs)

    def get(self, request, account_id):
        account = Account.objects.get(id=account_id)
        form = AccountTransferForm(account.id)
        context = {
            'form': form,
            'account': account,
        }
        return render(request, "common/account_transfer_form.html", context)

    def post(self, request, account_id):
        context = list()
        form = AccountTransferForm(account_id, request.POST)
        if form.is_valid():
            account_obj = Account.objects.get(id=account_id)
            account_obj.transactions.create(
                account=account_obj,
                amount=form.cleaned_data.get("amount"),
                transanction_type="withdraw",
                created_by=request.user
            )

            form.cleaned_data.get("to_account").transactions.create(
                account=form.cleaned_data.get("to_account"),
                amount=form.cleaned_data.get("amount"),
                transanction_type="deposit",
                created_by=request.user
            )

            # withdraw_transaction = AccountTransaction()
            # withdraw_transaction.account =
            # withdraw_transaction.amount = form.cleaned_data.get("amount")
            # withdraw_transaction.transanction_type = "withdraw"
            # withdraw_transaction.created_by = request.user
            # account_transaction.content_object = account
            # withdraw_transaction.save()

            # account_transaction = AccountTransaction()
            # account_transaction.account = form.cleaned_data.get("to_account")
            # account_transaction.amount = form.cleaned_data.get("amount")
            # account_transaction.transanction_type = "deposit"
            # account_transaction.created_by = request.user
            # account_transaction.content_object = account
            # account_transaction.save()
            info = {
                'status': True,
                'message': "Fund Transfer successfully done.."
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, "common/account_transfer_form.html",
                          {'form': form, 'account': Account.objects.get(id=account_id)})


class CashCollectionTransferView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CashCollectionTransferView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = CashCollectionTransferForm()
        context = {
            'other_payment_form': form,
        }
        return render(request, "common/cash_collection_transfer_form.html", context)

    def post(self, request):
        context = list()
        form = CashCollectionTransferForm(request.POST)
        if form.is_valid():
            payment = Payment()
            payment.payment_type = "other payment"
            payment.amount = form.cleaned_data.get("amount")
            payment.description = form.cleaned_data.get("description")
            payment.created_by = request.user
            payment.payment_branch = UserProfile.objects.filter(
                user=request.user).first().branch
            payment.save()
            payment.refresh_from_db()

            account_transaction = AccountTransaction()
            account_transaction.account = form.cleaned_data.get(
                "payment_method")
            account_transaction.transanction_type = "transfer"
            account_transaction.amount = form.cleaned_data.get("amount")
            account_transaction.created_by = request.user
            account_transaction.content_object = payment
            account_transaction.save()
            info = {
                'status': True,
                'message': "Money transfered successfully"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            print(form.errors)
            return render(request, "common/cash_collection_transfer_form.html", {'other_payment_form': form})


class NotePadView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotePadView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        notes = NotePad.objects.all()
        title = 'System Note Pad'
        context = {
            'title': title,
            'notes': notes,
        }
        return render(request, 'home/notepad.html', context)


class AddNote(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddNote, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        form = NotePadForm()
        title = 'ADD NOTE'
        context = {
            'title': title,
            'add_title': title,
            'form': form,
            'form_add': True,
        }
        return render(request, 'common/add_note.html', context)

    def post(self, request):
        context = list()
        form = NotePadForm(request.POST)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': 'Note Successful Saved!'
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, 'common/add_note.html',
                          {'form': form, 'add_title': 'Ops! Please try again!', 'form_add': True})


class EditNote(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditNote, self).dispatch(request, *args, **kwargs)

    def get(self, request, note_id):

        note = NotePad.objects.filter(id=note_id).first()
        form = NotePadForm(instance=note)
        title = 'EDIT NOTE'
        context = {
            'add_title': title,
            'form': form,
            'note': note,
            'form_add': False,
        }
        return render(request, 'common/edit_note.html', context)

    def post(self, request, note_id):
        note = NotePad.objects.filter(id=note_id).first()
        context = list()
        form = NotePadForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': 'Note Successful Edited!'
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            return render(request, 'common/edit_note.html', {'form': form, 'title': 'Ops! Please try again!'})


@never_cache
@login_required(login_url="/auth/login")
def delete_note(request, note_id):
    context = list()
    if NotePad.objects.filter(id=note_id).exists():
        NotePad.objects.filter(id=note_id).delete()
        if not NotePad.objects.filter(id=note_id).exists():
            info = {
                'status': True,
                'message': 'Note Deleted!',
            }
        else:
            info = {
                'status': False,
                'message': 'Failed to Deleted Note!'
            }
    else:
        info = {
            'status': False,
            'message': "Note's ID doesn't exists"
        }
    context.append(info)

    return HttpResponse(json.dumps(context))


class CustomerDebtReminderInfo(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CustomerDebtReminderInfo, self).dispatch(request, *args, **kwargs)

    def get(self, request, sale_id):
        title = 'Customer Sales Info'
        sale = Sale.objects.get(id=sale_id)
        sale_items = SaleItem.objects.filter(sale=sale)
        print(sale_items)
        profile = UserProfile.objects.get(user=sale.customer)
        context = {
            'title': title,
            'sale': sale,
            'sale_items': sale_items,
            'profile': profile,
        }
        return render(request, 'common/customer_debt_info.html', context)


def months(d1, d2):
    return d1.month - d2.month + 12 * (d1.year - d2.year)


def get_salary_month(request):
    months_choices = []
    staff_years = list(
        set([s.registered_date.year for s in UserProfile.objects.filter(user_type="Staff").filter(is_active=True)]))
    date_year = datetime.datetime.now().year
    for i in range(1, 13):
        months_choices.append(
            (i, datetime.date(date_year, i, 1).strftime('%B')))
    context = {
        "months_choices": months_choices,
        "years": sorted(staff_years)
    }
    return render(request, "common/salary_month.html", context)


class SalaryPaymentView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SalaryPaymentView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        selected_list = list()
        user_selected_list = json.loads(request.GET.get("user_selected_list"))
        staff_list = json.loads(request.GET.get("staff_list"))
        deduction_list = json.loads(request.GET.get("deduction_list"))
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        if request.GET.get("month"):
            month = request.GET.get("month")
        if request.GET.get("year"):
            year = request.GET.get("year")
        print(staff_list)
        print(deduction_list)
        print(user_selected_list)
        if len(user_selected_list) > 0:
            for staff, deduct, selected in zip(staff_list, deduction_list, user_selected_list):
                if selected:
                    staff_obj = UserProfile.objects.filter(id=staff).first()
                    if not Salary.objects.filter(Q(salary_date__year=year) & Q(salary_date__month=month)).filter(
                            staff=staff_obj.user).exists():
                        if deduct or deduct != 0:
                            deduction_amount = deduct
                        else:
                            deduction_amount = 0
                        selected_list.append({
                            "staff": staff_obj,
                            "deduct": deduction_amount
                        })
        else:
            for staff in UserProfile.objects.filter(user__is_staff=True).filter(
                    Q(registered_date__year__lte=year) & Q(registered_date__month__lte=month)).filter(
                user__is_superuser=False).exclude(user__in=[s.staff for s in Salary.objects.filter(
                    salary_date__year=year).filter(salary_date__month=month)]):
                if Payment.objects.filter(user=staff.user).filter(payment_type="staff loan").first():
                    deduction_amount = Payment.objects.filter(user=staff.user).filter(
                        payment_type="staff loan").first().deduction_amount
                else:
                    deduction_amount = 0

                selected_list.append({
                    "staff": staff,
                    "deduct": deduction_amount
                })
        form = SalaryForm()
        total_amount = sum(
            [get_staff_net_pay(s['staff'].pk, s['deduct'], month) for s in
             selected_list])
        context = {
            "total_amount": total_amount,
            "selected_list": selected_list,
            "form": form
        }
        return render(request, "common/salary_payment.html", context)

    def post(self, request, *args, **kwargs):
        context = list()
        try:
            not_selected_list = list()
            month = datetime.datetime.now().month
            if request.POST.get("month"):
                month = int(request.POST.get("month"))
            date_now = datetime.datetime(
                datetime.datetime.now().year, month, datetime.datetime.now().day)
            user_selected_list = json.loads(
                request.POST.get("user_selected_list"))
            print("======================================test3")
            print(user_selected_list)
            print("======================================test3")
            for select in user_selected_list:
                if select == False:
                    not_selected_list.append(select)
            if request.POST.get("payment_type") == "Bank":
                account_obj = Account.objects.filter(
                    id=request.POST.get("bank")).first()

                if total_account_amount(account_obj.pk) >= float(request.POST.get("total")):
                    print(user_selected_list)
                    if len(user_selected_list) == len(not_selected_list):
                        for marked, selected, deduct in zip(user_selected_list,
                                                            json.loads(
                                                                request.POST.get("staff_list")),
                                                            json.loads(request.POST.get("deduction_list"))):
                            user_profile_obj = UserProfile.objects.filter(
                                id=selected).first()
                            if deduct:
                                deduct = deduct
                            else:
                                deduct = 0
                            if user_profile_obj:
                                if user_profile_obj.salary_amount:
                                    salary_amount = user_profile_obj.salary_amount
                                else:
                                    salary_amount = 0
                            if not Salary.objects.filter(staff=user_profile_obj.user).filter(
                                    salary_date__month=month):
                                salary_obj = Salary()
                                salary_obj.staff = user_profile_obj.user
                                salary_obj.salary_date = date_now
                                salary_obj.salary_take_home = get_staff_net_pay(
                                    user_profile_obj.pk, deduct, month)
                                salary_obj.save()
                                salary_obj.refresh_from_db()
                                SalaryDeduction.objects.get_or_create(
                                    salary=salary_obj, amount=float(deduct))
                    else:
                        for marked, selected, deduct in zip(user_selected_list,
                                                            json.loads(
                                                                request.POST.get("staff_list")),
                                                            json.loads(request.POST.get("deduction_list"))):
                            if marked:
                                user_profile_obj = UserProfile.objects.filter(
                                    id=selected).first()
                                if deduct:
                                    deduct = deduct
                                else:
                                    deduct = 0
                                if user_profile_obj:
                                    if user_profile_obj.salary_amount:
                                        salary_amount = user_profile_obj.salary_amount
                                    else:
                                        salary_amount = 0
                                if not Salary.objects.filter(staff=user_profile_obj.user).filter(
                                        salary_date__month=month).exists():
                                    salary_obj = Salary()
                                    salary_obj.staff = user_profile_obj.user
                                    salary_obj.salary_date = date_now
                                    salary_obj.salary_take_home = get_staff_net_pay(
                                        user_profile_obj.pk, deduct, month)
                                    salary_obj.save()
                                    salary_obj.refresh_from_db()
                                    SalaryDeduction.objects.get_or_create(
                                        salary=salary_obj, amount=float(deduct))
                    account_transaction = AccountTransaction()
                    account_transaction.amount = request.POST.get("total")
                    account_transaction.transanction_type = "withdraw"
                    account_transaction.account = account_obj
                    account_transaction.created_by = request.user
                    account_transaction.save()
                    print(user_selected_list)
                    info = {
                        "status": True,
                        "message": "Successfully Paid"
                    }
                    context.append(info)
                    return HttpResponse(json.dumps(context))
                else:
                    info = {
                        "status": False,
                        "message": "Account has no enough balance!"
                    }
                    context.append(info)
                    return HttpResponse(json.dumps(context))
            else:
                if len(user_selected_list) == len(not_selected_list):
                    for marked, selected, deduct in zip(user_selected_list, json.loads(request.POST.get("staff_list")),
                                                        json.loads(request.POST.get("deduction_list"))):
                        user_profile_obj = UserProfile.objects.filter(
                            id=selected).first()
                        if deduct:
                            deduct = deduct
                        else:
                            deduct = 0
                        if user_profile_obj:
                            if user_profile_obj.salary_amount:
                                salary_amount = user_profile_obj.salary_amount
                            else:
                                salary_amount = 0
                        if not Salary.objects.filter(staff=user_profile_obj.user).filter(
                                salary_date__month=month):
                            salary_obj = Salary()
                            salary_obj.staff = user_profile_obj.user
                            salary_obj.salary_date = date_now
                            salary_obj.salary_take_home = (
                                get_staff_loan(user_profile_obj.user.pk) + float(deduct) + float(salary_amount))
                            salary_obj.save()
                            salary_obj.refresh_from_db()
                            SalaryDeduction.objects.get_or_create(
                                salary=salary_obj, amount=float(deduct))
                else:
                    for marked, selected, deduct in zip(user_selected_list, json.loads(request.POST.get("staff_list")),
                                                        json.loads(request.POST.get("deduction_list"))):
                        if marked:
                            user_profile_obj = UserProfile.objects.filter(
                                id=selected).first()
                            if deduct:
                                deduct = deduct
                            else:
                                deduct = 0
                            if user_profile_obj:
                                if user_profile_obj.salary_amount:
                                    salary_amount = user_profile_obj.salary_amount
                                else:
                                    salary_amount = 0
                            if not Salary.objects.filter(staff=user_profile_obj.user).filter(
                                    salary_date__month=month):
                                salary_obj = Salary()
                                salary_obj.staff = user_profile_obj.user
                                salary_obj.salary_date = date_now
                                salary_obj.salary_take_home = (
                                    get_staff_loan(user_profile_obj.user.pk) + float(deduct) + float(salary_amount))
                                salary_obj.save()
                                salary_obj.refresh_from_db()
                                SalaryDeduction.objects.get_or_create(
                                    salary=salary_obj, amount=float(deduct))
                userprofile = UserProfile.objects.filter(
                    user=request.user).first()
                expense = Expense()
                expense.expense_branch = userprofile.branch
                expense.authorized_by = userprofile
                expense.expense_for = "Salary "
                expense.save()
                expense.refresh_from_db()
                expenseDetail = ExpenseDetail()
                expenseDetail.expense
                expenseDetail.expense_amount = request.POST.get(
                    "total")
                expenseDetail.detail = "Salary"
                expenseDetail.save()
                info = {
                    "status": True,
                    "message": "Successfully Paid"
                }
                context.append(info)
                return HttpResponse(json.dumps(context))
        except Exception as e:
            print(e)
            info = {
                "status": False,
                "message": "Failed to Pay"
            }
            context.append(info)
        return HttpResponse(json.dumps(context))


def total_account_amount(account):
    deposits = \
        AccountTransaction.objects.filter(account__id=self.account).filter(transanction_type="deposit").aggregate(
            Sum('amount'))[
            "amount__sum"]
    withdraws = \
        AccountTransaction.objects.filter(account__id=self.account).filter(transanction_type="withdraw").aggregate(
            Sum('amount'))[
            "amount__sum"]
    if deposits:
        deposits = deposits
    else:
        deposits = 0
    if withdraws:
        withdraws = withdraws
    else:
        withdraws = 0
    if Account.objects.filter(id=account).first().opening_balance:
        opening_balance = float(Account.objects.filter(
            id=account).first().opening_balance)
    else:
        opening_balance = 0
    total = float(deposits + opening_balance) - float(withdraws)
    return total


class AttendenceFormView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AttendenceFormView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        date = None
        if request.GET.get("date"):
            date = datetime.datetime.strptime(
                str(request.GET.get("date")).strip(), "%d %B, %Y").date()

            if date:
                staffs = [s for s in UserProfile.objects.filter(
                    user__in=[s for s in User.objects.filter(is_active=True).filter(is_staff=True).filter(
                        is_superuser=False).filter(
                        id__in=[s.staff.pk for s in
                                Attendance.objects.filter(created__year=date.year).filter(created__day=date.day).filter(
                                    created__month=date.month)])])]
                not_attended = []
                if datetime.datetime.now().date() == date:
                    not_attended = [s for s in UserProfile.objects.filter(
                        user__in=[s for s in User.objects.filter(is_active=True).filter(is_staff=True).filter(
                            is_superuser=False).exclude(
                            id__in=[s.staff.pk for s in
                                    Attendance.objects.filter(created__year=date.year).filter(
                                        created__day=date.day).filter(
                                        created__month=date.month)])])]
                staffs = staffs + not_attended

            else:
                staffs = UserProfile.objects.filter(
                    user__in=[s for s in
                              User.objects.filter(is_active=True).filter(is_superuser=False).filter(is_staff=True)])
        else:
            staffs = UserProfile.objects.filter(
                user__in=[s for s in
                          User.objects.filter(is_active=True).filter(is_staff=True).filter(is_superuser=False)])
        title = 'Staff Attendence'
        form = AttendenceForm()
        context = {
            'title': title,
            "staffs": staffs,
            "form": form,
            "selected_date": date
        }
        return render(request, 'common/attendence_form.html', context)

    def post(self, request, *args, **kwargs):
        context = list()
        form = AttendenceForm(request.POST)
        if form.is_valid():
            staff_list = json.loads(request.POST.get("staff_list"))
            attend_list = json.loads(request.POST.get("attend_list"))
            time_list = json.loads(request.POST.get("time_list"))
            comment_list = json.loads(request.POST.get("comment_list"))
            for (staff, attend, comment, time) in zip(staff_list, attend_list, comment_list,
                                                      time_list):
                user_obj = UserProfile.objects.filter(id=staff).first()
                print(attend)
                if attend == True:
                    print("worked")
                    time = time
                else:
                    print("not worked")
                    time = ""
                if Attendance.objects.filter(created__date=datetime.datetime.now().date()).filter(
                        staff=user_obj.user).exists():
                    attendence_obj = Attendance.objects.filter(
                        created__date=datetime.datetime.now().date()).filter(staff=user_obj.user).first()
                    attendence_obj.time_in = time
                    attendence_obj.comment = comment
                    attendence_obj.save()
                    print(time)
                    print("========================test===================")
                else:
                    if attend:
                        time = time
                    else:
                        time = ""
                    attendence_obj = Attendance()
                    attendence_obj.staff = user_obj.user
                    attendence_obj.time_in = time
                    attendence_obj.comment = comment
                    attendence_obj.save()
            info = {
                "status": True,
                "message": "Successfuly Saved Attendence"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            info = {
                "status": False,
                "message": "Failed to Save Attendence"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))


class AttendenceView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AttendenceView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        staffs = UserProfile.objects.filter(
            user__in=[s for s in User.objects.filter(is_active=True).filter(is_staff=True)])
        title = 'Staff Attendence'
        form = AttendenceForm()
        context = {
            'title': title,
            "staffs": staffs,
            "form": form
        }
        return render(request, 'home/attendence.html', context)


class SalePerformanceView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SalePerformanceView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = 'Staff Sale Performance'
        staffs = UserProfile.objects.filter(user_type="Staff").filter(
            user__is_active=True).filter(is_active=True).filter(user__is_superuser=False)
        context = {
            'title': title,
            'staffs': staffs,
        }
        return render(request, 'home/sales_performance.html', context)


class StaffSaleDetailView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffSaleDetailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, staff_id):
        staff = User.objects.filter(id=staff_id).first()
        sale_list = Sale.objects.filter(staff=staff).order_by("-created")
        context = {
            'staff': staff,
            'sale_list': sale_list,
            'title': 'Staff Sales List Details'
        }
        return render(request, "home/staff_sale_details.html", context)


class CollectionPerformanceView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CollectionPerformanceView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        staffs = UserProfile.objects.filter(user_type="Staff").filter(
            user__is_active=True).filter(is_active=True).filter(user__is_superuser=False)
        title = 'Collection Performance'
        context = {
            'title': title,
            'staffs': staffs,
        }
        return render(request, 'home/collection_performance.html', context)


class StaffCollectionDetailView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffCollectionDetailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, staff_id):
        title = 'Staff Collection Performance'
        staff = User.objects.filter(id=staff_id).first()
        payments = Payment.objects.filter(collected_by=staff).order_by('-id')
        context = {
            'title': title,
            'payments': payments,
            'staff': staff,
        }
        return render(request, 'home/staff_collection_details.html', context)


class MonthlyEmployeeAssesmentView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MonthlyEmployeeAssesmentView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = 'Monthly Employee Assesment'
        staffs = UserProfile.objects.filter(
            user__in=[s for s in User.objects.filter(is_active=True).filter(is_staff=True).filter(is_superuser=False)])
        context = {
            'title': title,
            "staffs": staffs
        }
        return render(request, 'home/monthly_employee_assement.html', context)


class StaffMonthlyEmployeeAssementDetailView(View):
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffMonthlyEmployeeAssementDetailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        title = 'Staff Monthly Employee Assesment'
        user_obj = UserProfile.objects.filter(id=kwargs.get("pk")).first()
        not_attended_days = Attendance.objects.filter(
            staff=user_obj.user).filter(time_in=None)
        attended_days = Attendance.objects.filter(
            staff=user_obj.user).exclude(time_in=None)
        appended_attended_days = list()
        attended_day_count = len(
            Attendance.objects.filter(staff=user_obj.user).exclude(time_in=None).values_list("time_in"))
        if attended_day_count > 0:
            for s in attended_days:
                appended_attended_days.append(datetime.timedelta(
                    hours=s.time_in.hour, minutes=s.time_in.minute))
            average_time_in = sum(appended_attended_days, datetime.timedelta())
        else:
            average_time_in = 0
        customers = UserProfile.objects.filter(
            user_type="Customer").filter(added_by=user_obj.user)
        sales_items = list()
        total_quantity_counts = 0
        total_price_counts = list()
        if SaleItem.objects.filter(sale__in=[s for s in Sale.objects.filter(created_by=user_obj.user)]).distinct(
                "product__name"):
            total_quantity_counts = sum([s.quantity for s in SaleItem.objects.filter(
                sale__in=[s for s in Sale.objects.filter(created_by=user_obj.user)]).exclude(product=None)])
            for item in [s.product for s in
                         SaleItem.objects.filter(
                             sale__in=[s for s in Sale.objects.filter(created_by=user_obj.user)]).distinct(
                             "product__name")]:
                if item:
                    products_count = SaleItem.objects.filter(product__name=item.name).filter(
                        sale__in=[s for s in Sale.objects.filter(created_by=user_obj.user)]).count()
                    quantity = sum([s.quantity for s in SaleItem.objects.filter(product__name=item.name).filter(
                        sale__in=[s for s in Sale.objects.filter(created_by=user_obj.user)])])
                    price = sum([s.price for s in SaleItem.objects.filter(product__name=item.name).filter(
                        sale__in=[s for s in Sale.objects.filter(created_by=user_obj.user)])]) / products_count
                    sales_items.append({
                        "name": item.name,
                        "quantity": quantity,
                        "price": price,
                        "total": quantity * price
                    })
                    total_price_counts.append(quantity * price)
        context = {
            'title': title,
            "user_obj": user_obj,
            "sales_items": sales_items,
            "total_quantity_counts": total_quantity_counts,
            "total_price_counts": sum(total_price_counts),
            "not_attended_days": not_attended_days,
            "customers": customers,
            "average_time_in": average_time_in
        }
        return render(request, 'home/staff_monthly_assesment_detail.html', context)
