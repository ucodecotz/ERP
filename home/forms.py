from django import forms

from control.models import UserProfile, Account, AccountTransaction
from home.models import *
from django.utils.dateparse import parse_date
from django.db.models import Q
from control.models import Branch
from control.account_calculations import total_account_amount,get_total_cash_on_hand, get_today_total_cash_amount

class ProductForm(forms.ModelForm):
    """ProductForm definition."""

    class Meta:
        model = Product
        fields = [
            'name',
            'unit',
            'is_active',
        ]

    def __init__(self, form_update=False, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.form_update = form_update

    def clean(self):
        if not self.form_update:
            form_data = self.cleaned_data
            name = form_data.get("name", None)
            if Product.objects.filter(name=name).exists():
                self._errors['name'] = "This product exists.."

    def save(self, *args, **kwargs):
        product = super(ProductForm, self).save(*args, **kwargs)
        product.name = self.cleaned_data['name'].capitalize()
        product.unit = self.cleaned_data['unit'].upper()
        if not self.cleaned_data['is_active']:
            product.is_active = False
        product.save()
        return product


PAYMENT_TYPE_CHOICES = (
    ("Cash Collections", "Cash Collections"),
)


class PurchaseForm(forms.ModelForm):
    supplier_name = forms.ModelChoiceField(UserProfile.objects.filter(
        user_type="Supplier").filter(is_active=True), empty_label="Choose supplier")
    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, initial={
        'Cash Collections': 'Cash Collections'})

    class Meta:
        model = Purchase
        fields = [
            'supplier_name',
            'purchase_type',
            'receipt',
            'buying_price',
            'selling_price',
            'product',
            'quantity',
            'payment_method',
        ]

        widgets = {
            "purchase_type": forms.CheckboxInput()
        }

    def __init__(self, pk, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        data_list = list()
        data_list.append(("Cash Collections", "Cash Collections"))
        for s in [(s.pk, s) for s in Account.objects.all()]:
            data_list.append(s)
        data = tuple(data_list)
        self.fields['supplier_name'].required = True
        print("==========================test1")
        print(pk)
        print("==========================test1")
        if pk:
            self.fields['supplier_name'].initial = UserProfile.objects.filter(
                user_type="Supplier").filter(user__id=pk).filter(is_active=True).first()
        else:
            pass
        self.fields['receipt'].required = False
        self.fields['buying_price'].required = True
        self.fields['selling_price'].required = True
        self.fields['product'].required = True
        self.fields['product'].empty_label = "Choose product"
        self.fields['quantity'].required = True
        self.fields['payment_method'].choices = data


PAYMENT_TYPE_CHOICES = (
    ("Cash Collections", "Cash Collections"),
)


class SalesForm(forms.ModelForm):
    price = forms.DecimalField()
    quantity = forms.DecimalField()
    product = forms.ModelChoiceField( queryset=None, empty_label=None)
    customer_name = forms.ModelChoiceField(queryset=UserProfile.objects.filter(
        user__is_active=True).filter(user_type="Customer").filter(user__is_superuser=False).order_by("user__first_name"))
    staff_name = forms.ModelChoiceField(queryset=UserProfile.objects.filter(
        Q(user__is_active=True) & Q(user__is_staff=True)).filter(user_type="Staff").filter(user__is_superuser=False).order_by("user__first_name"))
    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, initial={
        'Cash Collections': 'Cash Collections'})

    class Meta:
        model = Sale
        fields = [
            'customer_name',
            'staff_name',
            'sale_type',
            'product',
            'price',
            'quantity',
            'sale_branch'
        ]

    def __init__(self, *args, **kwargs):
        super(SalesForm, self).__init__(*args, **kwargs)
        data_list = list()
        data_list.append(("Cash Collections", "Cash Collections"))
        for s in [(s.pk, s) for s in Account.objects.all()]:
            data_list.append(s)
        data = tuple(data_list)
        product_list = list()
        for product in Product.objects.all():
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
            if (total - total_sold_product) > 0:
                product_list.append(product)
        self.fields['product'].queryset = Product.objects.filter(id__in=[s.id for s in product_list]).order_by("name")
        self.fields['product'].required = True
        self.fields['customer_name'].required = True
        self.fields['customer_name'].empty_label = "Choose customer"
        self.fields['staff_name'].required = True
        self.fields['staff_name'].empty_label = "Choose staff"
        self.fields['price'].required = True
        self.fields['quantity'].required = True
        self.fields['sale_branch'].queryset = Branch.objects.all().order_by("name")
        self.fields['payment_method'].choices = data


class CustomerPaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, initial={
        'Cash Collections': 'Cash Collections'})
    account = forms.ModelChoiceField(queryset=Account.objects.filter(
        is_active=True).order_by("name"), required=False, empty_label="Choose transaction account")
    customer = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type="Customer").filter(
        is_active=True
    ).filter(user__is_superuser=False).order_by("user__first_name"), empty_label="Select customer")
    amount = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea())
    collected_by = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user__is_superuser=False).filter(user_type="Staff").filter(
        Q(user__is_staff=True) & Q(user__is_active=True)).order_by("user__first_name"), empty_label="Select Staff")

    def __init__(self, *args, **kwargs):
        super(CustomerPaymentForm, self).__init__(*args, **kwargs)
        data_list = list()
        data_list.append(("Cash Collections", "Cash Collections"))
        for s in [(s.pk, s) for s in Account.objects.all()]:
            data_list.append(s)
        data = tuple(data_list)
        self.fields['payment_method'].choices = data


class StaffCollectionForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, initial={
        'Cash Collections': 'Cash Collections'})
    staff = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user__is_superuser=False).filter(user_type="Staff").filter(
        Q(user__is_staff=True) & Q(user__is_active=True)), empty_label="Select Staff")
    amount = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea())
    collected_by = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user__is_superuser=False).filter(user_type="Staff").filter(
        Q(user__is_staff=True) & Q(user__is_active=True)), empty_label="Select Staff")

    def __init__(self, *args, **kwargs):
        super(StaffCollectionForm, self).__init__(*args, **kwargs)
        data_list = list()
        data_list.append(("Cash Collections", "Cash Collections"))
        for s in [(s.pk, s) for s in Account.objects.all()]:
            data_list.append(s)
        data = tuple(data_list)
        self.fields['payment_method'].choices = data


class LoanCollectionForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, initial={
        'Cash Collections': 'Cash Collections'})
    borrower = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user__is_superuser=False).filter(user_type="Borrower").filter(
        is_active=True
    ).order_by("user__first_name"), empty_label="Select Borrower")
    amount = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea())
    collected_by = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type="Staff").filter(user__is_superuser=False).filter(
        Q(user__is_staff=True) & Q(user__is_active=True)).order_by("user__first_name"), empty_label="Select Staff")
    authorized_by = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type="Staff").filter(user__is_superuser=False).filter(
        Q(user__is_staff=True) & Q(user__is_active=True)).order_by("user__first_name"), empty_label="Select Staff")

    def __init__(self, *args, **kwargs):
        super(LoanCollectionForm, self).__init__(*args, **kwargs)
        data_list = list()
        data_list.append(("Cash Collections", "Cash Collections"))
        for s in [(s.pk, s) for s in Account.objects.all()]:
            data_list.append(s)
        data = tuple(data_list)
        self.fields['payment_method'].choices = data


class SupplierPaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, initial={
        'Cash Collections': 'Cash Collections'})
    supplier = forms.ModelChoiceField(queryset=UserProfile.objects.filter(
        user_type="Supplier").filter(is_active=True).filter(user__is_superuser=False).order_by("user__first_name"), empty_label="Select supplier")
    amount = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super(SupplierPaymentForm, self).__init__(*args, **kwargs)
        data_list = list()
        data_list.append(("Cash Collections", "Cash Collections"))
        for s in [(s.pk, s) for s in Account.objects.all()]:
            data_list.append(s)
        data = tuple(data_list)
        self.fields['payment_method'].choices = data

    def clean(self):
        form_data = self.cleaned_data
        amount = form_data.get("amount", None)
        account_id = form_data.get("payment_method", None)
        if amount:
            if not account_id == "Cash Collections":
                if total_account_amount(int(account_id)) < amount:
                    self._errors['payment_method'] = "Your balance is not enough! transfer or recharge"
            else:
                if get_today_total_cash_amount() < amount:
                    self._errors['payment_method'] = "Your balance is not enough! transfer or recharge"


class OtherPaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, initial={
        'Cash Collections': 'Cash Collections'})
    amount = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super(OtherPaymentForm, self).__init__(*args, **kwargs)
        data_list = list()
        data_list.append(("Cash Collections", "Cash Collections"))
        for s in [(s.pk, s) for s in Account.objects.all()]:
            data_list.append(s)
        data = tuple(data_list)
        self.fields['payment_method'].choices = data

    def clean(self):
        form_data = self.cleaned_data
        amount = form_data.get("amount", None)
        account_id = form_data.get("payment_method", None)
        if amount:
            if not account_id == "Cash Collections":
                if total_account_amount(int(account_id)) < amount:
                    self._errors['payment_method'] = "Your balance is not enough! transfer or recharge"
            else:
                if get_today_total_cash_amount() < amount:
                    self._errors['payment_method'] = "Your balance is not enough! transfer or recharge"


class LoanProvisionForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, initial={
        'Cash Collections': 'Cash Collections'})
    borrower = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type="Borrower").filter(user__is_superuser=False).filter(
        is_active=True
    ).order_by("user__first_name"), empty_label="Select Borrower")
    amount = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea())
    collected_by = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type="Staff").filter(user__is_superuser=False).filter(
        Q(user__is_staff=True) & Q(user__is_active=True)).order_by("user__first_name"), empty_label="Select Staff")
    authorized_by = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type="Staff").filter(user__is_superuser=False).filter(
        Q(user__is_staff=True) & Q(user__is_active=True)).order_by("user__first_name"), empty_label="Select Staff")

    def __init__(self, *args, **kwargs):
        super(LoanProvisionForm, self).__init__(*args, **kwargs)
        data_list = list()
        data_list.append(("Cash Collections", "Cash Collections"))
        for s in [(s.pk, s) for s in Account.objects.all()]:
            data_list.append(s)
        data = tuple(data_list)
        self.fields['payment_method'].choices = data

    def clean(self):
        form_data = self.cleaned_data
        amount = form_data.get("amount", None)
        account_id = form_data.get("payment_method", None)
        if amount:
            if not account_id == "Cash Collections":
                if total_account_amount(int(account_id)) < amount:
                    self._errors['payment_method'] = "Your balance is not enough! transfer or recharge"
            else:
                if get_today_total_cash_amount() < amount:
                    self._errors['payment_method'] = "Your balance is not enough! transfer or recharge"



class StaffLoanForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, initial={
        'Cash Collections': 'Cash Collections'})
    staff = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type="Staff").filter(user__is_superuser=False).filter(
        Q(user__is_staff=True) & Q(user__is_active=True)
    ).order_by("user__first_name"), empty_label="Select Staff")
    amount = forms.DecimalField()
    deduction_amount = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea())
    collected_by = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type="Staff").filter(user__is_superuser=False).filter(
        Q(user__is_staff=True) & Q(user__is_active=True)).order_by("user__first_name"), empty_label="Select Staff")
    authorized_by = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type="Staff").filter(user__is_superuser=False).filter(
        Q(user__is_staff=True) & Q(user__is_active=True)).order_by("user__first_name"), empty_label="Select Staff")

    def __init__(self, *args, **kwargs):
        super(StaffLoanForm, self).__init__(*args, **kwargs)
        data_list = list()
        data_list.append(("Cash Collections", "Cash Collections"))
        for s in [(s.pk, s) for s in Account.objects.all()]:
            data_list.append(s)
        data = tuple(data_list)
        self.fields['payment_method'].choices = data
    

    def clean(self):
        form_data = self.cleaned_data
        amount = form_data.get("amount", None)
        account_id = form_data.get("payment_method", None)
        if amount:
            if not account_id == "Cash Collections":
                if self.total_account_amount(int(account_id)) < amount:
                    self._errors['payment_method'] = "Your balance is not enough! transfer or recharge"
            else:
                if get_today_total_cash_amount() < amount:
                    self._errors['payment_method'] = "Your balance is not enough! transfer or recharge"


class ExpenseForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, initial={
        'Cash Collections': 'Cash Collections'})
    detail = forms.CharField(max_length=200, required=True)
    expense_amount = forms.DecimalField(
        decimal_places=2, max_digits=15, min_value=0)

    class Meta:
        model = Expense
        fields = [
            'authorized_by',
            'expense_type',
            'staff',
            'asset',
            'detail',
            'expense_amount',
            'expense_for'
        ]

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['authorized_by'].queryset = UserProfile.objects.filter(
            Q(user__is_active=True) & Q(user__is_staff=True)).filter(user_type="Staff").filter(user__is_superuser=False).order_by("user__first_name")
        self.fields['authorized_by'].empty_label = "Choose staff"
        self.fields['staff'].queryset = UserProfile.objects.filter(
            Q(user__is_active=True) & Q(user__is_staff=True)).filter(user_type="Staff").filter(user__is_superuser=False).order_by("user__first_name")
        self.fields['staff'].empty_label = "Choose staff"
        self.fields['asset'].empty_label = "Choose asset"
        data_list = list()
        data_list.append(("Cash Collections", "Cash Collections"))
        for s in [(s.pk, s) for s in Account.objects.all()]:
            data_list.append(s)
        data = tuple(data_list)
        self.fields['payment_method'].choices = data
        if Account.objects.filter(name='PETTY CASH').exists():
            petty_id = Account.objects.filter(name='PETTY CASH').first().pk
            self.fields['payment_method'].initial = ( str(petty_id), "PETTY CASH")

    def clean(self):
        form_data = self.cleaned_data
        amount = form_data.get("expense_amount", None)
        account_id = form_data.get("payment_method", None)
        if amount:
            if not account_id == "Cash Collections":
                if total_account_amount(int(account_id)) < amount:
                    self._errors['payment_method'] = "Your balance is not enough! transfer or recharge"
            else:
                if get_today_total_cash_amount() < amount:
                    self._errors['payment_method'] = "Your balance is not enough! transfer or recharge"


class RORForm(forms.ModelForm):
    class Meta:
        model = ROR
        fields = [
            'name',
            's_price',
            'b_price',
        ]

    def save(self, *args, **kwargs):
        ror = super(RORForm, self).save(*args, **kwargs)
        ror.name = self.cleaned_data['name']
        ror.s_price = self.cleaned_data['s_price']
        ror.b_price = self.cleaned_data['b_price']
        ror.save()
        return ror
