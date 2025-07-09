"""
Module providing serializers and OpenAPI examples for vehicle endpoints.
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


class VehicleDataSerializer(serializers.Serializer):
    """
    Serializer for vehicle data structure.
    """

    vehicle_id = serializers.CharField(
        read_only=True, help_text="Unique identifier for the vehicle."
    )
    vehicle_name = serializers.CharField(help_text="Name of the vehicle.")
    vehicle_type = serializers.CharField(help_text="Type of the vehicle.")
    vehicle_number = serializers.CharField(
        help_text="Registration number of the vehicle."
    )
    vehicle_model = serializers.CharField(help_text="Model year of the vehicle.")
    vehicle_color = serializers.CharField(help_text="Color of the vehicle.")


class VehicleDataListSerializer(serializers.Serializer):
    """
    Serializer for the data list of vehicles.
    """

    list = VehicleDataSerializer(many=True, help_text="List of vehicles.")
    pagination = PaginationSerializer(
        help_text="Pagination information for the list of vehicles."
    )


class VehicleListResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of the vehicle list endpoint.
    """

    data = VehicleDataListSerializer(
        help_text="List of vehicles with pagination information."
    )
    errors = serializers.JSONField(
        help_text="Any errors for the response.", allow_null=True
    )
    messages = serializers.JSONField(
        help_text="Any informational messages for the response.", allow_null=True
    )
    status_code = serializers.IntegerField(default=200)
    is_success = serializers.BooleanField(default=True)


class VehicleResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of the vehicle detail endpoint.
    """

    data = VehicleDataSerializer(help_text="Vehicle information.")
    errors = serializers.JSONField(
        help_text="Any errors for the response.", allow_null=True
    )
    messages = serializers.JSONField(
        help_text="Any informational messages for the response.", allow_null=True
    )
    status_code = serializers.IntegerField(default=200)
    is_success = serializers.BooleanField(default=True)


# OpenAPI Examples

vehicle_example_data = {
    "vehicle_id": "777149a7-0caf-4f87-96f7-00184ff3e947",
    "vehicle_name": "Toyota Corolla",
    "vehicle_type": "Sedan",
    "vehicle_number": "KA01AB1234",
    "vehicle_model": "2021",
    "vehicle_color": "White",
}

Vehicle_create_success_example: OpenApiExample = get_create_success_example(
    "Successful Vehicle Creation",
    data=vehicle_example_data,
)

Vehicle_getById_success_example: OpenApiExample = get_by_id_success_example(
    name="Get Vehicle by Id - Success",
    data=vehicle_example_data,
)

vehicle_list_example_data = [vehicle_example_data]

Vehicle_list_success_example: OpenApiExample = get_list_success_example(
    name="List Vehicles - Success",
    list_data=vehicle_list_example_data,
)

Vehicle_update_success_example = get_update_success_example(
    name="Update Vehicle - Success",
    data={**vehicle_example_data, "vehicle_color": "Black"},
)

Vehicle_delete_success_example: OpenApiExample = get_delete_success_example(
    "Delete Vehicle - Success", "Vehicle deleted successfully."
)
