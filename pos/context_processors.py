from django.conf import settings
from django.db.models import Sum

from control.models import NotePad, UserProfile
from home.models import Sale, Payment


def return_system_name(request, *args, **kwargs):
    return {'sysname': settings.SYS_NAME}


def total_notes(request, *args, **kwargs):
    notes = NotePad.objects.all()

    return {'total_notes': notes.count()}


def credit_list(request, *args, **kwargs):
    credit_list = UserProfile.objects.filter(user_type="Customer").order_by("created")
    return {"all_credit_list": credit_list}
