"""
Invoice ViewSet
This module contains the InvoiceViewSet class, which is responsible for
handling HTTP requests related to invoices.
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

from ..db_access.invoice import invoice_manager
from ..serializers import (
    InvoiceSerializer,
    InvoiceResponseSerializer,
    InvoiceListResponseSerializer,
    Invoice_create_success_example,
    Invoice_getById_success_example,
    Invoice_list_success_example,
    Invoice_update_success_example,
    Invoice_delete_success_example,
)
from ..serializers.query import InvoiceQuerySerializer

from customer.db_access import customer_manager
from vehicle.db_access import vehicle_manager

MODULE_NAME = "Invoice"


class InvoiceViewSet(BaseView, viewsets.ViewSet):
    """
    ViewSet for handling invoice endpoints.
    """

    authentication_classes = get_authentication_classes()
    manager = invoice_manager
    serializer_class = InvoiceSerializer
    list_serializer_class = InvoiceQuerySerializer
    lookup_field = "invoice_id"
    search_fields = [
        "date",
        "status",
        "customer_type",
        "company_name",
        "first_name",
        "last_name",
        "vehicle_name",
        "vehicle_type",
        "vehicle_number",
    ]

    def get_list_query_object(self, query=None, **_):
        """
        Override to provide custom query object for listing invoices.
        """
        query_obj = {}

        company_type = query.pop("company_type", None)
        if company_type:
            query_obj["customer__company_type__icontains"] = company_type

        company_name = query.pop("company_name", None)
        if company_name:
            query_obj["customer__company_name__icontains"] = company_name

        first_name = query.pop("first_name", None)
        if first_name:
            query_obj["customer__first_name__icontains"] = first_name

        last_name = query.pop("last_name", None)
        if last_name:
            query_obj["customer__last_name__icontains"] = last_name

        vehicle_name = query.pop("vehicle_name", None)
        if vehicle_name:
            query_obj["vehicle__vehicle_name__icontains"] = vehicle_name

        vehicle_type = query.pop("vehicle_type", None)
        if vehicle_type:
            query_obj["vehicle__vehicle_type__icontains"] = vehicle_type

        return query_obj

    @extend_schema(
        responses={201: InvoiceResponseSerializer, **responses_400, **responses_401},
        examples=[
            Invoice_create_success_example,
            responses_400_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def create(self, request, *args, **kwargs):
        """Create a new invoice."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: InvoiceListResponseSerializer,
            **responses_404,
            **responses_401,
        },
        examples=[
            Invoice_list_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def list_all(self, request, *args, **kwargs):
        """List all invoices."""
        return super().list_all(request, *args, **kwargs)

    @extend_schema(
        responses={200: InvoiceResponseSerializer, **responses_404, **responses_401},
        examples=[
            Invoice_getById_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific invoice by its ID."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={200: InvoiceResponseSerializer, **responses_404, **responses_401},
        examples=[
            Invoice_update_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def update(self, request, *args, **kwargs):
        """Update an existing invoice."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        responses={204: InvoiceResponseSerializer, **responses_404, **responses_401},
        examples=[
            Invoice_delete_success_example,
            responses_404_example,
            responses_401_example,
        ],
        tags=[MODULE_NAME],
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an invoice."""
        return super().destroy(request, *args, **kwargs)

    def get_list(self, objects, request=None):
        """
        Convert a list of invoice objects to a list of dictionaries with
        additional customer and vehicle information.
        """
        customer_ids = [obj.customer_id for obj in objects]
        vehicle_ids = [obj.vehicle_id for obj in objects]

        customers_map = customer_manager.get_objects_mapping(
            query={"customer_id__in": customer_ids}, mapping_by="customer_id"
        )
        vehicles_map = vehicle_manager.get_objects_mapping(
            query={"vehicle_id__in": vehicle_ids}, mapping_by="vehicle_id"
        )

        data_list = []

        for obj in objects:
            obj_dict = obj.to_dict()
            obj_dict["vehicle"] = vehicles_map[obj.vehicle_id].to_dict()
            obj_dict["customer"] = customers_map[obj.customer_id].to_dict()
            data_list.append(obj_dict)

        return data_list
