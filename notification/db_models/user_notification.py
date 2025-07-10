from django.db import models

from utils.functions import get_uuid
from base.db_models.model import BaseModel


class UserNotification(BaseModel, models.Model):
    """
    UserNotifications model for mapping users to notifications.
    """

    user_notification_id = models.CharField(
        primary_key=True, default=get_uuid, max_length=128
    )
    user = models.ForeignKey(
        "auth_user.User", related_name="user_notifications", on_delete=models.CASCADE
    )
    notification = models.ForeignKey(
        "Notification", related_name="notifications", on_delete=models.CASCADE
    )

    is_read = models.BooleanField(default=False)

    class Meta:
        """
        db_table (str): Specifies the database table name for the model.
        """

        db_table = "user_notification_mapping"

    def to_dict(self):
        """
        Converts the UserNotifications instance to a dictionary representation.
        """
        return {
            "user_id": self.user_id,
            "is_read": self.is_read,
            "notification_id": self.notification_id,
            "user_notification_id": self.user_notification_id,
        }
