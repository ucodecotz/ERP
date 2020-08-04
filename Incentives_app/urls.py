from django.urls import path
from . import views

app_name = 'Incentives_app'
urlpatterns = [
    path('add_incentives/', views.AddIncentivesView.as_view(), name='add_incentives'),
    path('incentives_chart/', views.incentives_chart_view, name='incentives_chart'),
    path('individual_incentives_chart/', views.individual_incentives_chart, name='individual_incentives_chart')
]
