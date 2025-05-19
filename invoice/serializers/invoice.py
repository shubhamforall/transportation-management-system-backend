from rest_framework import serializers

from utils.messages import error
from utils.exceptions import codes

from invoice.db_access import invoice_manager


class InvoiceSerializer(serializers.Serializer):
    """
    Serializer for creating and updating invoice instances.
    """
    invoice_number = serializers.CharField(required=True, max_length=50)
    customer_id = serializers.CharField(required=True, max_length=36)
    vehicle_id = serializers.CharField(required=True, max_length=36)
    date = serializers.DateField(required=True)
    loading_address = serializers.CharField(required=True, max_length=255)
    delivery_address = serializers.CharField(required=True, max_length=255)
    weight = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    rate = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    total = serializers.DecimalField(required=True, max_digits=12, decimal_places=2)
    status = serializers.ChoiceField(choices=["PENDING", "PAID", "UNPAID"], required=True)

    def validate_invoice_number(self, value):
        """
        Validates that the invoice number is unique.
        - For creation: must not exist.
        - For update: must not exist on a different record.
        """
        is_update = self.instance is not None

        query = {"invoice_number": value}
        if is_update:
            query["invoice_id"] = {"NOT": self.instance.invoice_id}

        if invoice_manager.exists(query=query):
            raise serializers.ValidationError(
                error.ALREADY_EXIST,
                code=codes.DUPLICATE_ENTRY,
            )
        return value
