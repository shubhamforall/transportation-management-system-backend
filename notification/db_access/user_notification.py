"""
User Notification manager module.
This module contains the UserNotificationManager class, which
is responsible for managing the User Notification model.
"""

from base.db_access import manager
from ..db_models import UserNotification


class UserNotificationManager(manager.Manager[UserNotification]):
    """
    Manager class for the UserNotification model.
    """

    model = UserNotification


user_notification_manager = UserNotificationManager()
