"""
Module providing serializers and OpenAPI examples for payment endpoints.
"""

from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample
from utils.swagger import PaginationSerializer
from utils.swagger.common_swagger_functions import get_list_success_example


class PaymentDataSerializer(serializers.Serializer):
    """
    Serializer for payment data structure.
    """

    customer_id = serializers.CharField(help_text="Unique identifier for the customer.")
    full_name = serializers.CharField(help_text="Full name of the customer.")
    total_amount = serializers.FloatField(
        help_text="Total amount invoiced for the customer."
    )
    paid_amount = serializers.FloatField(help_text="Total amount paid by the customer.")
    pending_amount = serializers.FloatField(help_text="Remaining unpaid amount.")


class PaymentDataListSerializer(serializers.Serializer):
    """
    Serializer for the data list of payments.
    """

    list = PaymentDataSerializer(many=True, help_text="List of customer payments.")
    pagination = PaginationSerializer(
        help_text="Pagination information for the list of payments."
    )


class PaymentListResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of the payment list endpoint.
    """

    data = PaymentDataListSerializer(
        help_text="List of customer payments with pagination information."
    )
    errors = serializers.JSONField(
        help_text="Any errors for the response.", allow_null=True
    )
    messages = serializers.JSONField(
        help_text="Any informational messages for the response.", allow_null=True
    )
    status_code = serializers.IntegerField(default=200)
    is_success = serializers.BooleanField(default=True)


# OpenAPI Example

payment_example_data = {
    "customer_id": "57c35e7e-33d5-4253-b94e-0ad68991d95c",
    "full_name": "Shubham Patil",
    "total_amount": 21883.76,
    "paid_amount": 0,
    "pending_amount": 21883.76,
}

payment_list_example_data = [payment_example_data]

Payment_list_success_example: OpenApiExample = get_list_success_example(
    name="List Payments - Success",
    list_data=payment_list_example_data,
)
