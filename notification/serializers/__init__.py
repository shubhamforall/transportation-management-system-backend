from .user_notification import MarkAsReadRequestSerializer

from .swagger import (
    NotificationListResponseSerializer,
    MarkAsReadResponseSerializer,
    notification_list_success_example,
    mark_as_read_success_example,
    mark_as_read_warning_example,
)

__all__ = [
    "MarkAsReadRequestSerializer",
    "NotificationListResponseSerializer",
    "MarkAsReadResponseSerializer",
    "notification_list_success_example",
    "mark_as_read_success_example",
    "mark_as_read_warning_example",
]
