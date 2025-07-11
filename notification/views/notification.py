"""
Notification ViewSet
This module contains the NotificationViewSet class, which is responsible for
handling HTTP requests related to notifications.
"""

from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema

from base.views.base import UpdateView, ListView
from authentication import get_authentication_classes
from utils.constants import MethodEnum
from utils.response import generate_response
from utils.swagger import (
    responses_400,
    responses_404,
    responses_401,
    responses_400_example,
    responses_404_example,
    responses_401_example,
)

from ..serializers import MarkAsReadRequestSerializer
from ..serializers import (
    NotificationListResponseSerializer,
    MarkAsReadResponseSerializer,
    notification_list_success_example,
    mark_as_read_success_example,
    mark_as_read_warning_example,
)
from ..db_access import user_notification_manager, notification_manager

MODULE = "Notification"


class NotificationViewSet(UpdateView, ListView, viewsets.ViewSet):
    """
    ViewSet for managing invoices.
    """

    authentication_classes = get_authentication_classes()
    serializer_class = MarkAsReadRequestSerializer
    manager = user_notification_manager

    @classmethod
    def get_method_view_mapping(cls):
        return {
            **UpdateView.get_method_view_mapping(patch=False),
            **ListView.get_method_view_mapping(),
        }

    def get_list_query_object(self, request=None, **kwargs):
        """
        Override the method to return the query object for listing notifications.
        This method is used to filter notifications based on user_id.
        """
        return {"user_id": request.user.user_id, "is_read": False}

    @extend_schema(
        responses={
            200: NotificationListResponseSerializer,
            **responses_404,
            **responses_401,
        },
        examples=[
            notification_list_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE],
    )
    def list_all(self, request, *args, **kwargs):
        return super().list_all(request, *args, **kwargs)

    def get_list(self, objects, **_):
        notification_ids = []
        for obj in objects:
            notification_ids.append(obj.notification_id)

        notification_data = notification_manager.get_objects_mapping(
            query={"notification_id__in": notification_ids},
            mapping_by="notification_id",
        )

        data_list = []

        for obj in objects:
            data_dict = {}
            data_dict["notification"] = notification_data[obj.notification_id].to_dict()
            data_list.append(data_dict)

        return data_list

    @extend_schema(
        responses={
            200: MarkAsReadResponseSerializer,
            **responses_400,
            **responses_404,
            **responses_401,
        },
        examples=[
            mark_as_read_success_example,
            mark_as_read_warning_example,
            responses_400_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE],
    )
    def update(self, request, *args, **kwargs):
        """
        This function will make  is_read flag false -> true so the notification will be mark as read and wont
        be seen in the notification list.
        """
        request_data = request.data
        # add the validator for the request data. only mark_all_as_read and list_of_notification_id fields are allowed

        serializer = MarkAsReadRequestSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        mark_all_as_read = validated_data.get("mark_all_as_read", False)

        query = {
            "user_id": request.user.user_id,
        }
        if not mark_all_as_read:
            query["notification_id__in"] = request_data["list_of_notification_id"]

        user_notifications = self.manager.list(query)

        count = user_notifications.count()
        if not count:
            return generate_response(
                messages={
                    "message": "Please provide the notification id",  # add the message in the utils.message.warning module create the warning module
                    "type": "warning",  # make a enum for these add warning, error, info, success put it into the utils.constants module
                }
            )

        user_notifications.update(is_read=True)

        return generate_response(
            status_code=status.HTTP_200_OK,
            messages={
                "message": f"{count} Messages marked as read!...",  # add the message in the utils.message.success module
            },
        )
