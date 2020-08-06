from django.conf import settings
from django.db import models
from home.models import *


# TODO employee/staff model here from all staff
class staff_incentives(models.Model):
    staff_name = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name_plural = '1: Staff with'


class ProductIncentives(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    inncentive_amount = models.CharField(max_length=255)
    start_date = models.DateTimeField(default=timezone.now, null=True)
    end_date = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = '2: Incentives'

    def __str__(self):
        return str(self.products.name)


class Incentives_chart(models.Model):
    sales_table = models.ForeignKey(Sale, on_delete=models.DO_NOTHING, null=True)
    staff_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        verbose_name_plural = '3: Incentives chart'

    def __str__(self):
        return self.staff_name
