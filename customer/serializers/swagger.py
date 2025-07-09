"""
Module providing serializers and OpenAPI examples for customer endpoints.
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


class CustomerDataSerializer(serializers.Serializer):
    """
    Serializer for customer data structure.
    """

    customer_id = serializers.CharField(
        read_only=True, help_text="Unique identifier for the customer."
    )
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


class CustomerDataListSerializer(serializers.Serializer):
    """
    Serializer for the data list of customers.
    """

    list = CustomerDataSerializer(many=True, help_text="List of customers.")
    pagination = PaginationSerializer(
        help_text="Pagination information for the list of customers."
    )


class CustomerListResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of the customer list endpoint.
    """

    data = CustomerDataListSerializer(
        help_text="List of customers with pagination information."
    )
    errors = serializers.JSONField(
        help_text="Any errors for the response.", allow_null=True
    )
    messages = serializers.JSONField(
        help_text="Any informational messages for the response.", allow_null=True
    )
    status_code = serializers.IntegerField(default=200)
    is_success = serializers.BooleanField(default=True)


class CustomerResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of the customer detail endpoint.
    """

    data = CustomerDataSerializer(help_text="Customer information.")
    errors = serializers.JSONField(
        help_text="Any errors for the response.", allow_null=True
    )
    messages = serializers.JSONField(
        help_text="Any informational messages for the response.", allow_null=True
    )
    status_code = serializers.IntegerField(default=200)
    is_success = serializers.BooleanField(default=True)


# OpenAPI Examples

customer_example_data = {
    "customer_id": "57c35e7e-33d5-4253-b94e-0ad68991d95c",
    "customer_type": "INDIVIDUAL",
    "company_name": None,
    "first_name": "First",
    "last_name": "Last",
    "full_name": "First Last",
    "mobile_number": "9876543210",
    "email": "user@example.com",
    "address": "1234 Main Street, City, State",
}

Customer_create_success_example: OpenApiExample = get_create_success_example(
    "Successful Customer Creation",
    data=customer_example_data,
)

Customer_getById_success_example: OpenApiExample = get_by_id_success_example(
    name="Get Customer by Id - Success",
    data=customer_example_data,
)

customer_list_example_data = [customer_example_data]

Customer_list_success_example: OpenApiExample = get_list_success_example(
    name="List Customers - Success",
    list_data=customer_list_example_data,
)

Customer_update_success_example = get_update_success_example(
    name="Update Customer - Success",
    data={**customer_example_data, "mobile_number": "9123456789"},
)

Customer_delete_success_example: OpenApiExample = get_delete_success_example(
    "Delete Customer - Success", "Customer deleted successfully."
)
