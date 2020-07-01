from control.models import *
from django import forms
from decimal import Decimal
from django.db.models import Sum


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name']

    def __init__(self, form_update=False, *args, **kwargs):
        super(RegionForm, self).__init__(*args, **kwargs)
        self.form_update = form_update

    def clean(self):
        if not self.form_update:
            form_data = self.cleaned_data
            name = form_data.get("name", None)
            if Region.objects.filter(name=name).exists():
                self._errors['name'] = "This region exists"

    def save(self, *args, **kwargs):
        region = super(RegionForm, self).save(*args, **kwargs)
        region.name = self.cleaned_data['name'].capitalize()
        region.save()
        return region


class BranchForm(forms.ModelForm):
    """BranchForm definition."""

    class Meta:
        model = Branch
        fields = [
            'name',
            'region',
            'phone_number',
            'street'
        ]

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        self.fields['region'].empty_label = "Choose branch region"

    def save(self, *args, **kwargs):
        branch = super(BranchForm, self).save(*args, **kwargs)
        branch.name = self.cleaned_data['name'].capitalize()
        branch.street = self.cleaned_data['street'].capitalize()
        branch.save()
        return branch


class AssetForm(forms.ModelForm):
    """Form definition for Asset."""

    class Meta:
        """Meta definition for Assetform."""

        model = Asset
        fields = [
            'name',
            'asset_number',
            'condition',
            'branch',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['asset_number'].required = False
        self.fields['condition'].required = True
        self.fields['branch'].required = True
        self.fields['branch'].empty_label = "Choose asset branch"
        self.fields['description'].required = False

    def save(self, *args, **kwargs):
        asset = super(AssetForm, self).save(*args, **kwargs)
        asset.name = self.cleaned_data['name'].capitalize()
        asset.save()
        return asset


class UserTypeForm(forms.ModelForm):
    """Form definition for UserType."""

    class Meta:
        """Meta definition for UserTypeform."""

        model = UserType
        fields = ['name']

    def save(self, *args, **kwargs):
        utype = super(UserTypeForm, self).save(*args, **kwargs)
        utype.name = self.cleaned_data['name'].capitalize()
        utype.save()
        return utype


class AccountForm(forms.ModelForm):
    """Form definition for Account."""

    class Meta:
        """Meta definition for Accountform."""
        model = Account
        fields = ['name', 'number', 'branch','opening_balance']

    def __init__(self, form_update=False, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['branch'].empty_label = "Choose branch"
        self.form_update = form_update
        self.fields['opening_balance'].required = False

    def clean(self):
        if not self.form_update:
            form_data = self.cleaned_data
            number = form_data.get("number", None)
            if Account.objects.filter(number=number).exists():
                self._errors['number'] = "This Account number exists"

    def save(self, *args, **kwargs):
        account = super(AccountForm, self).save(*args, **kwargs)
        account.name = self.cleaned_data['name'].upper()
        account.number = self.cleaned_data['number']
        account.branch = self.cleaned_data['branch']
        account.opening_balance = self.cleaned_data['opening_balance']
        account.save()
        return account


class NotePadForm(forms.ModelForm):
    class Meta:
        model = NotePad
        fields = ['title', 'description', 'created_by', 'priority']

    def save(self, *args, **kwargs):
        notepad = super(NotePadForm, self).save(*args, **kwargs)
        notepad.title = self.cleaned_data['title'].upper()
        notepad.description = self.cleaned_data['description']
        notepad.created_by = self.cleaned_data['created_by']
        notepad.priority = self.cleaned_data['priority']
        notepad.save()
        return notepad


PAYMENT_TYPE = (
    ("Bank", "Bank"),
    ("Cash In Hand", "Cash In Hand")
)


class SalaryForm(forms.Form):
    payment_type = forms.ChoiceField(
        choices=PAYMENT_TYPE, initial=("Bank", "Bank"))
    bank = forms.ModelChoiceField(queryset=Account.objects.filter(is_active=True), empty_label=None)

    def __init__(self, form_update=False, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)
        self.fields['bank'].required = False
        self.fields['payment_type'].required = True


class AccountTransanctionForm(forms.ModelForm):
    class Meta:
        model = AccountTransaction
        fields = [
            'amount',
            'transanction_type',
        ]


class AccountTransferForm(forms.Form):
    amount = forms.DecimalField(min_value=1, required=True)
    to_account = forms.ModelChoiceField(queryset=Account.objects.filter(is_active=True))


    def __init__(self, account, *args, **kwargs):
        from control.account_calculations import total_account_amount
        super(AccountTransferForm, self).__init__(*args, **kwargs)
        self.account = account
        self.fields['to_account'].queryset = Account.objects.filter(is_active=True).exclude(id=self.account)
        self.fields['to_account'].empty_label = "Choose Account to transfer"
        self.fields['amount'].max_value = total_account_amount(self.account)

    def clean(self):
        form_data = self.cleaned_data
        amount = form_data.get("amount", None)
        if amount:
            from control.account_calculations import total_account_amount
            if total_account_amount(self.account) < amount:
                self._errors['amount'] = "Your balance is not enough!"

class CashCollectionTransferForm(forms.Form):
    payment_method = forms.ModelChoiceField(queryset=Account.objects.filter(is_active=True))
    amount = forms.DecimalField()
    description = forms.CharField(widget=forms.Textarea())

    
    def __init__(self, *args, **kwargs):
        super(CashCollectionTransferForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].empty_label = "Choose Account"
    
    def clean(self):
        form_data = self.cleaned_data
        amount = form_data.get("amount", None)
        from control.account_calculations import get_today_total_cash_amount,get_total_cash_on_hand
        if amount:
            if get_total_cash_on_hand() < amount:
                self._errors['amount'] = "Your balance is not enough!"


class AttendenceForm(forms.Form):
    attend = forms.BooleanField()
    time_in = forms.CharField()
    comment = forms.CharField(max_length=500)

    def __init__(self, *args, **kwargs):
        super(AttendenceForm, self).__init__(*args, **kwargs)
        self.fields['attend'].required = False
        self.fields['time_in'].required = False
        self.fields['comment'].required = False
