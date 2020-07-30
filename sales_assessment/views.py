from django.shortcuts import render


# Create your views here.
def assessment_View(request):
    return render(request, 'sales_assessment.html')


def analytics(request):
    return render(request, 'sales_assessment_analytics.html')
