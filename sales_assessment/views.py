from django.shortcuts import render


# Create your views here.
def add_incentives_view(request):
    return render(request, 'add_incentives.html')


def incentives_chart_view(request):
    return render(request, 'incentives_chart.html')

def individual_incentivites_chart(request):
    return render(request, 'individual_incentives_chart.html')
