from .db_access import notification_manager, user_notification_manager


class Notification:

    manager = notification_manager

    def __init__(self, title, message, notification_type, notification_data=None):
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.notification_data = notification_data

    def __create(self):
        """
        Create a notification in the database.
        """
        return self.manager.create(
            data={
                "title": self.title,
                "message": self.message,
                "notification_type_id": self.notification_type,
                "notification_data": self.notification_data,
            }
        )

    def send_notification(self, user_ids: str | list[str]):
        """
        Send the notification to a specific user.
        """

        if not user_ids:
            return False

        if isinstance(user_ids, str):
            user_ids = [user_ids]

        notification = self.__create()

        user_notification_manager.create(
            [
                {
                    "user_id": user_id,
                    "notification_id": notification.notification_id,
                }
                for user_id in user_ids
            ],
            many=True,
        )

        return True
