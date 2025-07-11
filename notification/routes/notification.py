"""
Notification URL routing module.
"""

from django.urls import path

from ..views import NotificationViewSet

urlpatterns = [
    path(
        "notifications",
        NotificationViewSet.as_view(NotificationViewSet.get_method_view_mapping()),
        name="notification",
    )
]
