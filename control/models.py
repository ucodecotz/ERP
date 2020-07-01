from django.db import models
from django.contrib.auth.models import User
from datetime import *
from datetime import datetime, timedelta
from django.utils import timezone
import decimal
from django.apps import config
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
import math


class ModelIsDeletable(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def is_deletable(self):
        # get all the related object
        for rel in self._meta.get_fields():
            try:
                # check if there is a relationship with at least one related object
                related = rel.related_model.objects.filter(
                    **{rel.field.name: self})
                if related.exists():
                    # if there is return a Tuple of flag = False the related_model object
                    return False, related
            except AttributeError:  # an attribute error for field occurs when checking for AutoField
                pass  # just pass as we dont need to check for AutoField
        return True, None

    def whenpublished(self):
        now = timezone.now()
        diff = now - self.created
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = int(math.floor(diff.days / 30))
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = int(math.floor(diff.days / 365))
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

    def whenupdated(self):
        now = timezone.now()
        diff = now - self.updated
        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = int(math.floor(diff.days / 30))
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = int(math.floor(diff.days / 365))
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

    class Meta:
        abstract = True


class UserType(ModelIsDeletable):
    """Model definition for UserType."""
    name = models.CharField(max_length=200)

    class Meta:
        """Meta definition for UserType."""

        verbose_name = 'UserType'
        verbose_name_plural = 'UserTypes'

    def __str__(self):
        """Unicode representation of UserType."""
        return self.name


USER_TYPE_CHOICES = (
    ("Customer", "Customer"),
    ("Borrower", "Borrower"),
    ("Supplier", "Supplier"),
    ("Staff", "Staff"),
)


class UserProfile(ModelIsDeletable):
    """Model definition for UserProfile."""
    user = models.ForeignKey(
        User, related_name="profile", on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=100, choices=USER_TYPE_CHOICES, default="Staff")
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    credit_limit = models.CharField(max_length=200, null=True, blank=True)
    credit_day = models.IntegerField(null=True, blank=True)
    balance = models.CharField(max_length=200, blank=True, null=True)
    salary_amount = models.DecimalField(
        decimal_places=2, max_digits=15, default=0)
    added_by = models.ForeignKey(
        User, related_name="added_by", on_delete=models.DO_NOTHING, null=True, blank=True)
    branch = models.ForeignKey(
        'Branch', related_name="user_branch", null=True, blank=True, on_delete=models.CASCADE)
    registered_date = models.DateField(default=timezone.now)

    class Meta:
        """Meta definition for UserProfile."""

        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        """Unicode representation of UserProfile."""
        return str(self.user.first_name) + " " + str(self.user.last_name)

    def get_staff_branch(self):
        if self.branch:
            return str(self.branch.name)


class Region(ModelIsDeletable):
    name = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = u'Region'
        verbose_name_plural = u'Regions'
        permissions = (
            ("block_region", "Can Block Region"),
            ("unblock_region", "Can Unblock Region"),
        )

    def __str__(self):
        return self.name


class Branch(ModelIsDeletable):
    """Model definition for Branch."""
    name = models.CharField(max_length=200)
    region = models.ForeignKey(
        Region, related_name="branch_region", on_delete=models.DO_NOTHING)
    manager = models.ForeignKey(
        User, related_name="branch_manager", on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        """Meta definition for Branch."""

        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        """Unicode representation of Branch."""
        return self.name


class Attendance(ModelIsDeletable):
    """Model definition for Attendance."""
    staff = models.ForeignKey(
        User, related_name="attendant", on_delete=models.CASCADE)
    time_in = models.CharField(max_length=20, blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)
    comment = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        """Meta definition for Attendance."""

        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    def __str__(self):
        """Unicode representation of Attendance."""
        return str(self.staff)


ASSET_CONDITION_COICES = (
    ("working", "working"),
    ("not working", "not working")
)


class Asset(ModelIsDeletable):
    """Model definition for Asset."""
    name = models.CharField(max_length=200)
    asset_number = models.CharField(max_length=200, null=True, blank=True)
    condition = models.CharField(
        max_length=100, choices=ASSET_CONDITION_COICES, default="working")
    description = models.TextField(max_length=500, blank=True, null=True)
    branch = models.ForeignKey(
        Branch, related_name="asset_branch", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Asset."""

        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'

    def __str__(self):
        """Unicode representation of Asset."""
        return self.name


class Salary(ModelIsDeletable):
    """Model definition for Salary."""
    staff = models.ForeignKey(
        User, related_name="staff_salary", on_delete=models.CASCADE)
    salary_take_home = models.DecimalField(
        decimal_places=2, max_digits=15, default=0)
    salary_date = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta definition for Salary."""

        verbose_name = 'Salary'
        verbose_name_plural = 'Salaries'

    def __str__(self):
        """Unicode representation of Salary."""
        return str(self.staff.first_name)


class Account(ModelIsDeletable):
    """Model definition for Account."""
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    opening_balance = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    branch = models.ForeignKey(
        Branch, related_name="branch_account", on_delete=models.CASCADE)
    transactions = GenericRelation("AccountTransaction")

    class Meta:
        """Meta definition for Account."""

        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        """Unicode representation of Account."""
        return self.name + " " + str(self.number)


ACCOUNT_TRANSACTION_TYPES = (
    ("deposit", "deposit"),
    ("withdraw", "withdraw"),
    ("transfer", "transfer"),
)


class AccountTransaction(ModelIsDeletable):
    """Model definition for AccountTransaction."""
    account = models.ForeignKey(Account, related_name="transanction_bank",
                                on_delete=models.DO_NOTHING, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    transanction_type = models.CharField(
        max_length=100, choices=ACCOUNT_TRANSACTION_TYPES, default="deposit")
    created_by = models.ForeignKey(
        User, related_name="transaction_personel", on_delete=models.DO_NOTHING)
    transanction_date = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        """Meta definition for AccountTransaction."""

        verbose_name = 'AccountTransaction'
        verbose_name_plural = 'AccountTransactions'

    def __str__(self):
        """Unicode representation of AccountTransaction."""
        return str(self.account.name)


class NotePad(ModelIsDeletable):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='note_reated_by', on_delete=models.DO_NOTHING)
    priority = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Note Pad'
        verbose_name_plural = 'Note Pads'

    def __str__(self):
        return self.title


class SalaryDeduction(ModelIsDeletable):
    salary = models.ForeignKey(
        Salary, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0)
