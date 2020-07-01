from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from control.models import Branch, UserProfile
from home.models import BadDebt
from django.db.models import Q
from control.customer_calculation import get_customer_debt


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', ]


class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        self.cleaned_data = super(LogInForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user_obj = authenticate(username=username, password=password)
        if user_obj is None:
            raise forms.ValidationError('Wrong credentials please try again!')


class CustomerForm(forms.Form):
    full_name = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    location = forms.CharField(required=False)
    credit_day = forms.IntegerField(required=False)
    credit_limit = forms.CharField(required=False)
    balance = forms.CharField(required=False)
    added_by = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type="Staff").filter(
        Q(user__is_staff=True) & Q(user__is_active=True)).filter(user__is_superuser=False), empty_label="Choose Staff")

    def __init__(self, form_update=False, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].required = True
        self.fields['email'].required = False
        self.fields['phone_number'].required = False
        self.fields['location'].required = False
        self.fields['credit_day'].required = False
        self.fields['credit_limit'].required = False
        self.fields['added_by'].required = True
        self.fields['balance'].required = False
        self.form_update = form_update

    def clean(self):
        if not self.form_update:
            form_data = self.cleaned_data
            email = form_data.get("email", None)
            if not User.objects.filter(email=email):
                if User.objects.filter(email=email).exists():
                    self._errors['email'] = "This Email exists"


class SupplierForm(forms.Form):
    full_name = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    location = forms.CharField(required=False)
    balance = forms.CharField(required=False)

    def __init__(self, form_update=False, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].required = True
        self.fields['email'].required = False
        self.fields['phone_number'].required = False
        self.fields['location'].required = False
        self.form_update = form_update

    def clean(self):
        if not self.form_update:
            form_data = self.cleaned_data
            email = form_data.get("email", None)
            if not User.objects.filter(email=email):
                if User.objects.filter(email=email).exists():
                    self._errors['email'] = "This Email exists"


class BorrowerForm(forms.Form):
    full_name = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    location = forms.CharField(required=False)
    balance = forms.CharField(required=False)

    def __init__(self, form_update=False, *args, **kwargs):
        super(BorrowerForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].required = True
        self.fields['email'].required = False
        self.fields['phone_number'].required = False
        self.fields['location'].required = False
        self.form_update = form_update

    def clean(self):
        if not self.form_update:
            form_data = self.cleaned_data
            email = form_data.get("email", None)
            if not User.objects.filter(email=email):
                if User.objects.filter(email=email).exists():
                    self._errors['email'] = "This Email exists"


class StaffForm(forms.Form):
    full_name = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    salary = forms.CharField(required=True)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label="Choose staff branch", required=True)
    role = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Choose staff role", required=True)
    balance = forms.CharField(required=False)
    
    def __init__(self, form_update=False, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.form_update = form_update

    def clean(self):
        if not self.form_update:
            form_data = self.cleaned_data
            email = form_data.get("email", None)
            if not User.objects.filter(email=email):
                if User.objects.filter(email=email).exists():
                    self._errors['email'] = "This Email exists"


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

    def save(self, *args, **kwargs):
        group = super(UserGroupForm, self).save(*args, **kwargs)
        group.name = self.cleaned_data['name'].capitalize()
        group.save()
        return group


DEBT_TYPE_CHOICES = (
    ("Expense", "Expense"),
    ("Staff", "Staff")
)


class BadDebtForm(forms.ModelForm):
    """Form definition for BadDebt."""
    debt_type = forms.ChoiceField(choices=DEBT_TYPE_CHOICES, widget=forms.Select(), required=True, initial="Expense")

    class Meta:
        """Meta definition for BadDebtform."""
        model = BadDebt
        fields = [
            'customer',
            'staff',
            'amount',
            'description',
            'debt_type',
        ]

    def __init__(self, pk, *args, **kwargs):
        super(BadDebtForm, self).__init__(*args, **kwargs)
        self.fields['staff'].queryset = UserProfile.objects.filter(user_type="Staff").filter(
            user__is_active=True).filter(is_active=True).filter(user__is_superuser=False)
        self.fields['staff'].empty_label = "Choose staff"
        self.fields['customer'].disabled = True
        self.fields['customer'].queryset = UserProfile.objects.filter(user__id=pk).filter(user__is_superuser=False)
        self.fields['customer'].empty_label = None
        self.fields['amount'].max_value = get_customer_debt(pk)
        self.fields['amount'].initial = get_customer_debt(pk)
