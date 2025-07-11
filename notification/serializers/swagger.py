"""
Module providing serializers and OpenAPI examples for notification endpoints.
"""

from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample

from utils.swagger import PaginationSerializer
from utils.swagger.common_swagger_functions import (
    get_update_success_example,
    get_list_success_example,
)

from ..constants import NotificationTypes


class NotificationDataSerializer(serializers.Serializer):
    """
    Serializer for notification data structure.
    """

    notification_id = serializers.CharField(
        help_text="Unique identifier for the notification."
    )
    title = serializers.CharField(
        help_text="Title of the notification.", allow_blank=True
    )
    message = serializers.CharField(
        help_text="Content of the notification.", allow_blank=True
    )
    notification_data = serializers.JSONField(
        help_text="Additional data for the notification.", allow_null=True
    )
    notification_type_id = serializers.ChoiceField(
        choices=NotificationTypes.choices, help_text="Type of the notification."
    )


class NotificationListDataSerializer(serializers.Serializer):
    """
    Serializer for the data field in notification list response.
    """

    list = NotificationDataSerializer(many=True, help_text="List of notifications.")
    pagination = PaginationSerializer(help_text="Pagination info.")


class NotificationListResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of the notification list endpoint.
    """

    data = NotificationListDataSerializer(
        help_text="Notifications list and pagination."
    )
    errors = serializers.JSONField(
        help_text="Any errors in the response.", allow_null=True
    )
    messages = serializers.JSONField(
        help_text="Any informational messages returned.", allow_null=True
    )
    status_code = serializers.IntegerField(default=200)
    is_success = serializers.BooleanField(default=True)


class MarkAsReadResponseSerializer(serializers.Serializer):
    """
    Serializer for mark-as-read PUT response.
    """

    data = serializers.JSONField(
        help_text="Usually null or additional data if needed.", allow_null=True
    )
    errors = serializers.JSONField(help_text="Error messages if any.", allow_null=True)
    messages = serializers.JSONField(help_text="Success or warning message.")
    status_code = serializers.IntegerField(default=200)
    is_success = serializers.BooleanField(default=True)


notification_example_data = {
    "notification_id": "c1a6e36f-85dd-47b2-b248-e1a96e2a8dfe",
    "title": "Welcome Notification",
    "message": "Thank you for signing up!",
    "notification_data": {"key": "value"},
    "notification_type_id": "INVOICE",
}

notification_list_success_example: OpenApiExample = get_list_success_example(
    name="Notification List - Success", list_data=[notification_example_data]
)

mark_as_read_success_example: OpenApiExample = get_update_success_example(
    name="Mark Notifications as Read - Success",
    data=None,
    message={"message": "3 Messages marked as read!..."},
)

mark_as_read_warning_example: OpenApiExample = get_update_success_example(
    name="Mark Notifications as Read - Warning",
    data=None,
    message={"message": "Please select the notification", "type": "warning"},
)
