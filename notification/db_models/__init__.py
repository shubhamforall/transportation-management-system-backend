"""
This module contains the database models for the notification app.
It imports the Notification model from the notification module.
"""

from .notification import Notification
from .user_notification import UserNotification

__all__ = ["Notification", "UserNotification"]
