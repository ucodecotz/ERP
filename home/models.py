from django.db import models
from django.contrib.auth.models import User
from datetime import *
from datetime import datetime, timedelta

from django.db.models import Sum
from django.utils import timezone
import decimal
import math
from django.contrib.contenttypes.fields import GenericRelation
from control.models import ModelIsDeletable, Asset, UserProfile, AccountTransaction


class MyManager(models.Manager):

    def date_obj(self, date=datetime.now()):
        items = []
        for obj in self.all():
            if datetime(obj.purchase_date):
                items.append(obj)
        return items


class Product(ModelIsDeletable):
    """Model definition for Product."""
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return self.name

    def remaining_stock(self):
        total = Purchase.objects.filter(product=self).aggregate(
            Sum('quantity'))['quantity__sum']
        if not total:
            total = 0
        total_sold_product = SaleItem.objects.filter(
            product=self).aggregate(Sum('quantity'))['quantity__sum']
        if not total_sold_product:
            total_sold_product = 0
        return total - total_sold_product


PURCHASE_TYPE_CHOICES = (
    ("cash", "cash"),
    ("credit", "credit")
)


class Purchase(ModelIsDeletable):
    """Model definition for Purchase."""
    supplier = models.ForeignKey(
        User, related_name="supplier", on_delete=models.DO_NOTHING)
    purchase_type = models.BooleanField(default=False)
    # purchase_date = models.CharField(max_length=100, null=True, blank=True)
    purchase_date = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(
        User, related_name="authorized_by", on_delete=models.DO_NOTHING, null=True, blank=True)
    purchase_branch = models.ForeignKey(
        'control.Branch', related_name="purchase_branch", on_delete=models.DO_NOTHING, null=True, blank=True)
    receipt = models.FileField(
        upload_to='uploads/%Y/%m/%d/', max_length=100, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    product = models.ForeignKey(
        Product, related_name="purchased_product", on_delete=models.DO_NOTHING, null=True, blank=True)
    selling_price = models.DecimalField(
        decimal_places=2, max_digits=15, default=0)
    buying_price = models.DecimalField(
        decimal_places=2, max_digits=15, default=0)
    quantity = models.IntegerField(default=1)
    purchase = GenericRelation(AccountTransaction)

    class Meta:
        """Meta definition for Purchase."""

        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

    def __str__(self):
        return str(self.supplier)

    def format_date(self, year, month, day):
        return Purchase.objects.filter(id=self.id).filter()


SALE_TYPE_CHOICES = (
    ("cash", "cash"),
    ("credit", "credit")
)


class Sale(ModelIsDeletable):
    """Model definition for Sale."""
    customer = models.ForeignKey(
        User, related_name="customer", on_delete=models.DO_NOTHING)
    sale_type = models.BooleanField(default=False)
    sale_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(
        decimal_places=2, max_digits=15, default=0)
    amount_paid = models.DecimalField(
        decimal_places=2, max_digits=15, default=0)
    staff = models.ForeignKey(
        User, related_name="staff", on_delete=models.DO_NOTHING)
    sale_branch = models.ForeignKey(
        'control.Branch', related_name="sale_branch", on_delete=models.DO_NOTHING, null=True, blank=True)
    created_by = models.ForeignKey(
        User, related_name="authorization", on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=500, blank=True, null=True)
    waiting_approval = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User, related_name="approved_by", on_delete=models.DO_NOTHING, null=True, blank=True)
    sale = GenericRelation(AccountTransaction, related_query_name='sales')

    class Meta:
        """Meta definition for Sale."""

        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __str__(self):
        """Unicode representation of Sale."""
        return str(self.customer)


class SaleItem(ModelIsDeletable):
    """Model definition for SaleItem."""
    sale = models.ForeignKey(
        Sale, related_name="sale_info", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="purchased_item", on_delete=models.DO_NOTHING, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    quantity = models.IntegerField()

    class Meta:
        """Meta definition for SaleItem."""

        verbose_name = 'SaleItem'
        verbose_name_plural = 'SaleItems'

    def __str__(self):
        if self.product:
            return str(self.product.name) + ' ' + str(self.quantity)


EXPENSE_TYPE_CHOICES = (
    ("normal", "normal"),
    ("asset", "asset"),
    ("staff", "staff")
)


class Expense(ModelIsDeletable):
    """Model definition for Expense."""
    expense_type = models.CharField(
        max_length=200, choices=EXPENSE_TYPE_CHOICES, default="normal")
    staff = models.ForeignKey(UserProfile, related_name="for_staff",
                              on_delete=models.DO_NOTHING, null=True, blank=True)
    expense_date = models.DateField(default=timezone.now)
    expense_branch = models.ForeignKey(
        'control.Branch', related_name="expense_branch", on_delete=models.DO_NOTHING, null=True, blank=True)
    authorized_by = models.ForeignKey(
        UserProfile, related_name="created_by", on_delete=models.CASCADE)
    asset = models.ForeignKey('control.Asset', related_name="for_asset",
                              null=True, blank=True, on_delete=models.DO_NOTHING)
    expense_for = models.CharField(max_length=200, null=True, blank=True)
    expense = GenericRelation(AccountTransaction)

    class Meta:
        """Meta definition for Expense."""

        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def __str__(self):
        return str(self.expense_type)


class ExpenseDetail(ModelIsDeletable):
    expense = models.ForeignKey(
        Expense, on_delete=models.CASCADE, null=True, blank=True)
    detail = models.CharField(max_length=200, null=True, blank=True)
    expense_amount = models.DecimalField(
        decimal_places=2, max_digits=15, default=0)


PAYMENT_TYPE_CHOICES = (
    ("customer payment", "customer payment"),
    ("staff collection", "staff collection"),
    ("loan collection",  "loan collection"),
    ("supplier payment", "supplier payment"),
    ("other payment",    "other payment"),
    ("loan provision",   "loan provision"),
    ("staff loan",       "staff loan"),
)


class Payment(ModelIsDeletable):
    payment_type = models.CharField(
        max_length=200, choices=PAYMENT_TYPE_CHOICES, default="customer payment")
    user = models.ForeignKey(User, related_name="payment_to",
                             on_delete=models.DO_NOTHING, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    deduction_amount = models.DecimalField(
        decimal_places=2, max_digits=15, default=0)
    payment_date = models.DateTimeField(default=timezone.now)
    authorized_by = models.ForeignKey(User, related_name="payment_authorized_by", on_delete=models.DO_NOTHING,
                                      blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="payment_created_by", on_delete=models.DO_NOTHING, blank=True,
                                   null=True)
    collected_by = models.ForeignKey(User, related_name="payment_collector", on_delete=models.DO_NOTHING, blank=True,
                                     null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    payment_branch = models.ForeignKey(
        'control.Branch', related_name="payment_branch", on_delete=models.DO_NOTHING, null=True, blank=True)
    payment = GenericRelation(AccountTransaction, related_query_name='payments')

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return str(self.payment_type)


class ROR(ModelIsDeletable):
    name = models.CharField(max_length=200, blank=False)
    b_price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    s_price = models.DecimalField(decimal_places=2, max_digits=20, default=0)

    class Meta:
        verbose_name = 'ROR'
        verbose_name_plural = 'RORs'

    def __str__(self):
        return str(self.name)


class BadDebt(ModelIsDeletable):
    """Model definition for BadDebt."""
    customer = models.ForeignKey(
        UserProfile, related_name="debtor", blank=True, null=True, on_delete=models.DO_NOTHING)
    staff = models.ForeignKey(UserProfile, related_name="charged_to", on_delete=models.DO_NOTHING, null=True,
                              blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    description = models.TextField(max_length=300)

    class Meta:
        """Meta definition for BadDebt."""

        verbose_name = 'BadDebt'
        verbose_name_plural = 'BadDebts'

    def __str__(self):
        """Unicode representation of BadDebt."""
        return str(self.staff)
