
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('auth/', include('sys_auth.urls')),
    path('control/',include('control.urls')),
    path('reports/',include('report.urls')),
    path('sales_assessments/',include('sales_assessment.urls')),
]
