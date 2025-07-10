"""
Notification manager module.
This module contains the NotificationManager class, which
is responsible for managing the Notification model.
"""

from base.db_access import manager
from ..db_models import Notification


class NotificationManager(manager.Manager[Notification]):
    """
    Manager class for the Notification model.
    """

    model = Notification


notification_manager = NotificationManager()
