"""
Vehicle ViewSet
This module contains the VehicleViewSet class, which is responsible for
handling HTTP requests related to vehicles.
"""

from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from authentication import get_authentication_classes

from base.views import BaseView
from utils.swagger import (
    responses_400,
    responses_404,
    responses_401,
    responses_400_example,
    responses_404_example,
    responses_401_example,
)

from ..db_access.vehicle import vehicle_manager
from ..serializers import (
    VehicleSerializer,
    VehicleResponseSerializer,
    VehicleListResponseSerializer,
    Vehicle_create_success_example,
    Vehicle_getById_success_example,
    Vehicle_list_success_example,
    Vehicle_update_success_example,
    Vehicle_delete_success_example,
)

MODULE_NAME = "Vehicle"


class VehicleViewSet(BaseView, viewsets.ViewSet):
    """
    ViewSet for handling vehicle endpoints.
    """

    authentication_classes = get_authentication_classes()
    manager = vehicle_manager
    serializer_class = VehicleSerializer
    lookup_field = "vehicle_id"

    @extend_schema(
        responses={201: VehicleResponseSerializer, **responses_400, **responses_401},
        examples=[
            Vehicle_create_success_example,
            responses_400_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def create(self, request, *args, **kwargs):
        """Create a new vehicle."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: VehicleListResponseSerializer,
            **responses_404,
            **responses_401,
        },
        examples=[
            Vehicle_list_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def list_all(self, request, *args, **kwargs):
        """List all vehicles."""
        return super().list_all(request, *args, **kwargs)

    @extend_schema(
        responses={200: VehicleResponseSerializer, **responses_404, **responses_401},
        examples=[
            Vehicle_getById_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a vehicle by its ID."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={200: VehicleResponseSerializer, **responses_404, **responses_401},
        examples=[
            Vehicle_update_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def update(self, request, *args, **kwargs):
        """Update a vehicle by its ID."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        responses={204: VehicleResponseSerializer, **responses_404, **responses_401},
        examples=[
            Vehicle_delete_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a vehicle by its ID."""
        return super().destroy(request, *args, **kwargs)
