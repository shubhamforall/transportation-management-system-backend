""" "
Notification URL Configuration
This module defines the URL patterns for the notification application.
"""

from django.urls import path, include

urlpatterns = [path("", include("notification.routes.notification"))]
