"""
URL configuration for the Support Ticket System.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tickets/', include('tickets.urls')),
]
