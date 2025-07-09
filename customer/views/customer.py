"""
Customer ViewSet
This module contains the CustomerViewSet class, which is responsible for
handling HTTP requests related to customers.
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

from ..db_access.customer import customer_manager
from ..serializers import (
    CustomerSerializer,
    CustomerResponseSerializer,
    CustomerListResponseSerializer,
    Customer_create_success_example,
    Customer_getById_success_example,
    Customer_list_success_example,
    Customer_update_success_example,
    Customer_delete_success_example,
)

MODULE_NAME = "Customer"


class CustomerViewSet(BaseView, viewsets.ViewSet):
    """
    ViewSet for handling customer endpoints.
    """

    authentication_classes = get_authentication_classes()
    manager = customer_manager
    serializer_class = CustomerSerializer
    lookup_field = "customer_id"

    @extend_schema(
        responses={201: CustomerResponseSerializer, **responses_400, **responses_401},
        examples=[
            Customer_create_success_example,
            responses_400_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def create(self, request, *args, **kwargs):
        """Create a new customer."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: CustomerListResponseSerializer,
            **responses_404,
            **responses_401,
        },
        examples=[
            Customer_list_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def list_all(self, request, *args, **kwargs):
        """List all customers."""
        return super().list_all(request, *args, **kwargs)

    @extend_schema(
        responses={200: CustomerResponseSerializer, **responses_404, **responses_401},
        examples=[
            Customer_getById_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a customer by ID."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={200: CustomerResponseSerializer, **responses_404, **responses_401},
        examples=[
            Customer_update_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def update(self, request, *args, **kwargs):
        """Update an existing customer."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        responses={204: CustomerResponseSerializer, **responses_404, **responses_401},
        examples=[
            Customer_delete_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a customer by ID."""
        return super().destroy(request, *args, **kwargs)
