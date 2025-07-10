"""
Notification model for storing notification details.
"""

from django.db import models

from utils.functions import get_uuid
from base.db_models.model import BaseModel


from ..constants import NotificationTypes


class Notification(BaseModel):
    """
    Notification model for storing notification details.
    """

    notification_id = models.CharField(
        primary_key=True, default=get_uuid, max_length=128
    )

    title = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    notification_data = models.JSONField(null=True, blank=True)
    notification_type_id = models.CharField(
        max_length=64, choices=NotificationTypes.choices
    )

    class Meta:
        """
        db_table (str): Specifies the database table name for the model.
        """

        db_table = "notification"

    def to_dict(self):
        """
        Converts the notification instance to a dictionary representation.
        """

        return {
            "title": self.title,
            "message": self.message,
            "notification_id": self.notification_id,
            "notification_data": self.notification_data,
            "notification_type": self.notification_type_id,
        }
