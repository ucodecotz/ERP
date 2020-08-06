from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.views.generic import View
from home.models import Product
from Incentives_app.models import *
from django.forms import modelformset_factory


# Create your views here.

class AddIncentivesView(View):
    def get(self, *args, **kwargs):
        product_qs = Product.objects.filter()[:4]
        product_incentives_qs = ProductIncentives.objects.all()[:4]
        addForm = modelformset_factory(Product, fields =('name', 'inncentive_amount', 'isIncentive'))
        form = addForm()
        context = {
            'products': product_qs,
            'form':form,
            'product_incentives':product_incentives_qs
        }
        return render(self.request, 'add_incentives.html', context)


    def post(self, *args, **kwargs):
        addForm = modelformset_factory(Product, fields =('name', 'inncentive_amount', 'isIncentive'))
        if self.request.method == 'POST':
            form = addForm(self.request.POST)
            instance = form.save()
            

       
       
        return redirect('Incentives_app:add_incentives')

    # def post(self, *args, **kwargs):
    #     if not self.request.POST.has_key('strName'):
    #         return ""
    #     if self.request.POST['strName']:
    #         #   another alternatives
    #         self.request.POST.getlist('recommendations')
    #         some_var = self.request.POST.getlist('checks[]')

    #         return ','.join(self.request.POST.getlist('strName'))

    #     else:
    #         return ""


def incentives_chart_view(request):
    return render(request, 'incentives_chart.html')


def individual_incentives_chart(request):
    return render(request, 'individual_incentives_chart.html')


class IncentivesView(View):
    def get(self , *args, **kwargs):
        product_qs = Product.objects.filter()[:4]
        product_incentives_qs = ProductIncentives.objects.all()[:4]
        context = {
            'products': product_qs,
            'product_incentives':product_incentives_qs
        }
        return render(self.request,'edit_incentives.html', context)


from django.forms import CheckboxSelectMultiple, CheckboxInput, DateInput, TextInput
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from funky_sheets.formsets import HotView

from .models import *


def index(request):
    return HttpResponseRedirect(reverse('update'))



def add_Icnt(request):
    addForm = modelformset_factory(Product, fields =('name', 'unit', 'isIncentive'))
    if request.method == 'POST':
        form = addForm(request.POST)
        instance = form.save()

   
    form = addForm()
    context = {
        'from':form
    }
    return render(request, 'add_incentives.html', context)