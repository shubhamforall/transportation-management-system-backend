"""
Module providing serializers and OpenAPI examples for invoice endpoints.
"""

from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample
from utils.swagger import PaginationSerializer
from utils.swagger.common_swagger_functions import (
    get_delete_success_example,
    get_update_success_example,
    get_create_success_example,
    get_list_success_example,
    get_by_id_success_example,
)


class InvoiceCustomerSerializer(serializers.Serializer):
    customer_id = serializers.CharField(help_text="Unique identifier for the customer.")
    customer_type = serializers.CharField(
        help_text="Type of the customer (e.g., INDIVIDUAL or ORGANIZATION)."
    )
    company_name = serializers.CharField(
        allow_null=True, required=False, help_text="Company name if applicable."
    )
    first_name = serializers.CharField(help_text="First name of the customer.")
    last_name = serializers.CharField(help_text="Last name of the customer.")
    full_name = serializers.CharField(help_text="Full name of the customer.")
    mobile_number = serializers.CharField(help_text="Mobile number of the customer.")
    email = serializers.EmailField(help_text="Email address of the customer.")
    address = serializers.CharField(help_text="Address of the customer.")


class InvoiceVehicleSerializer(serializers.Serializer):
    vehicle_id = serializers.CharField(help_text="Unique identifier for the vehicle.")
    vehicle_name = serializers.CharField(help_text="Name of the vehicle.")
    vehicle_type = serializers.CharField(
        help_text="Type of the vehicle (e.g., Sedan, Truck)."
    )
    vehicle_number = serializers.CharField(
        help_text="Registration number of the vehicle."
    )
    vehicle_model = serializers.CharField(help_text="Model year of the vehicle.")
    vehicle_color = serializers.CharField(help_text="Color of the vehicle.")


class InvoiceDataSerializer(serializers.Serializer):
    """
    Serializer for invoice data structure.
    """

    invoice_id = serializers.CharField(
        read_only=True, help_text="Unique identifier for the invoice."
    )
    customer = InvoiceCustomerSerializer(
        help_text="Customer associated with the invoice."
    )
    vehicle = InvoiceVehicleSerializer(help_text="Vehicle associated with the invoice.")
    date = serializers.DateField(help_text="Date of the invoice.")
    loading_address = serializers.CharField(
        help_text="Loading address for the invoice."
    )
    delivery_address = serializers.CharField(
        help_text="Delivery address for the invoice."
    )
    weight = serializers.FloatField(help_text="Weight of the shipment in kilograms.")
    rate = serializers.FloatField(help_text="Rate per unit weight.")
    total = serializers.FloatField(help_text="Total calculated amount.")
    status = serializers.CharField(
        help_text="Current status of the invoice (e.g., PENDING, APPROVED)."
    )


class InvoiceDataListSerializer(serializers.Serializer):
    """
    Serializer for the data list of invoices.
    """

    list = InvoiceDataSerializer(many=True, help_text="List of invoices.")
    pagination = PaginationSerializer(
        help_text="Pagination information for the list of invoices."
    )


class InvoiceListResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of the invoice list endpoint.
    """

    data = InvoiceDataListSerializer(
        help_text="List of invoices with pagination information."
    )
    errors = serializers.JSONField(
        help_text="Any errors for the response.", allow_null=True
    )
    messages = serializers.JSONField(
        help_text="Any informational messages for the response.", allow_null=True
    )
    status_code = serializers.IntegerField(default=200, help_text="HTTP status code.")
    is_success = serializers.BooleanField(
        default=True, help_text="Indicates if the request was successful."
    )


class InvoiceResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of the invoice detail endpoint.
    """

    data = InvoiceDataSerializer(help_text="Invoice details.")
    errors = serializers.JSONField(
        help_text="Any errors for the response.", allow_null=True
    )
    messages = serializers.JSONField(
        help_text="Any informational messages for the response.", allow_null=True
    )
    status_code = serializers.IntegerField(default=200, help_text="HTTP status code.")
    is_success = serializers.BooleanField(
        default=True, help_text="Indicates if the request was successful."
    )


# OpenAPI Examples

invoice_example_data = {
    "invoice_id": "a096a0a5-8fa6-450d-8713-4d34464efb1e",
    "customer": {
        "customer_id": "57c35e7e-33d5-4253-b94e-0ad68991d95c",
        "customer_type": "INDIVIDUAL",
        "company_name": None,
        "first_name": "First",
        "last_name": "Last",
        "full_name": "First Last",
        "mobile_number": "9876543210",
        "email": "user@example.com",
        "address": "1234 Main Street, City, State",
    },
    "vehicle": {
        "vehicle_id": "777149a7-0caf-4f87-96f7-00184ff3e947",
        "vehicle_name": "Toyota Corolla",
        "vehicle_type": "Sedan",
        "vehicle_number": "KA01AB1234",
        "vehicle_model": "2021",
        "vehicle_color": "White",
    },
    "date": "2024-05-15",
    "loading_address": "Warehouse A, Industrial Area",
    "delivery_address": "Retail Store B, City Center",
    "weight": 1250.5,
    "rate": 8.75,
    "total": 10941.88,
    "status": "PENDING",
}

Invoice_create_success_example: OpenApiExample = get_create_success_example(
    "Successful Invoice Creation",
    data=invoice_example_data,
)

Invoice_getById_success_example: OpenApiExample = get_by_id_success_example(
    name="Get Invoice by Id - Success",
    data=invoice_example_data,
)

Invoice_list_success_example: OpenApiExample = get_list_success_example(
    name="List Invoices - Success",
    list_data=[invoice_example_data],
)

Invoice_update_success_example: OpenApiExample = get_update_success_example(
    name="Update Invoice - Success",
    data={**invoice_example_data, "status": "APPROVED"},
)

Invoice_delete_success_example: OpenApiExample = get_delete_success_example(
    "Delete Invoice - Success", "Invoice deleted successfully."
)
