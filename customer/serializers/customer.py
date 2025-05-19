"""
This module imports the Customer class from the customer module
and makes it available for use in other parts of the application.
"""

from rest_framework import serializers

from utils.messages import error
from utils.exceptions import codes

from customer.db_access import customer_manager


class CustomerSerializer(serializers.Serializer):
    """
    Serializer for both creating and updating a customer.
    """

    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    mobile_number = serializers.CharField(required=True, max_length=15)
    email = serializers.EmailField(required=True, max_length=100)
    address = serializers.CharField(required=True, max_length=255)

    def validate_email(self, value):
        """
        Validate email field.
        - For create: email must not exist.
        - For update: email must not belong to a different customer.
        """

        is_update = self.instance is not None

        query = {"email": value}
        if is_update:
            query["customer_id"] = {"NOT": self.instance.customer_id}

        if customer_manager.exists(query=query):
            raise serializers.ValidationError(
                error.ALREADY_EXIST,
                code=codes.DUPLICATE_ENTRY,
            )

        return value
