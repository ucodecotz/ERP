from django.urls import path
from . import views
app_name = 'sales_assessment'
urlpatterns = [
    path('sales_assessment/', views.assessment_View, name='sales_assessment'),
    path('sales_assessment_analytics/', views.analytics, name='sales_assessment_analytics')
]
