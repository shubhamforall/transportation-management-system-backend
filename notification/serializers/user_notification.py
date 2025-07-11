from rest_framework import serializers
from utils.exceptions import codes


class MarkAsReadRequestSerializer(serializers.Serializer):
    mark_all_as_read = serializers.BooleanField(required=False, default=False)
    list_of_notification_id = serializers.ListField(
        child=serializers.CharField(max_length=128), required=False
    )

    def validate(self, data):
        """
        Ensure that list_of_notification_id is provided when mark_all_as_read is False.
        Also ensure no extra fields are passed.
        """
        if not data.get("mark_all_as_read", False):
            if not data.get("list_of_notification_id"):
                raise serializers.ValidationError(
                    {"list_of_notification_id": self.error_messages["required"]},
                    code=codes.REQUIRED,
                )

        return data
