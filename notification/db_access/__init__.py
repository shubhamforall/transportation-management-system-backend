"""
This module provides access to the database for the notification module.
It imports the NotificationManager class from the notification module.
"""

from .notification import notification_manager
from .user_notification import user_notification_manager

__all__ = ["notification_manager", "user_notification_manager"]
