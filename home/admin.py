from django.contrib import admin
from home.models import *

admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Expense)
admin.site.register(Payment)
admin.site.register(BadDebt)
admin.site.register(ExpenseDetail)