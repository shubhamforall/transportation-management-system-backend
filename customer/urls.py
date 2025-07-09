"""
URL configuration for the customer app.

"""

from django.urls import path, include

urlpatterns = [path("", include("customer.routes.customer"))]
