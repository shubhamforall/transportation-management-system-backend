from rest_framework import serializers

from utils.messages import error
from utils.exceptions import codes

from invoice.db_access import invoice_manager


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

