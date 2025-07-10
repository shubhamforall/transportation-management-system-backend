from rest_framework import serializers

from utils.messages import error
from utils.exceptions import codes

from customer.db_access import customer_manager
from vehicle.db_access import vehicle_manager


class InvoiceSerializer(serializers.Serializer):
    """
    Serializer for creating and updating invoice instances.
    """

    customer_id = serializers.UUIDField(required=True)
    vehicle_id = serializers.UUIDField(required=True)
    date = serializers.DateField(required=True)
    loading_address = serializers.CharField(required=True, max_length=255)
    delivery_address = serializers.CharField(required=True, max_length=255)
    weight = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    rate = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    total = serializers.DecimalField(required=True, max_digits=12, decimal_places=2)
    status = serializers.ChoiceField(
        choices=["PENDING", "PAID", "UNPAID"], required=True
    )

    def validate_customer_id(self, value):
        """
        Validate the given customer ID. If the customer ID does not exist in the database,
        raises serializers.ValidationError.
        """
        if not customer_manager.exists(query={"customer_id": value}):
            raise serializers.ValidationError(
                error.NO_DATA_FOUND,
                code=codes.NO_DATA_FOUND,
            )
        return value

    def validate_vehicle_id(self, value):
        """
        Validate the given vehicle ID. If the vehicle ID does not exist in the database,
        raises serializers.ValidationError.
        """
        if not vehicle_manager.exists(query={"vehicle_id": value}):
            raise serializers.ValidationError(
                error.NO_DATA_FOUND,
                code=codes.NO_DATA_FOUND,
            )
        return value
