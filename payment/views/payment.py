"""
Payment ViewSet
This module contains the PaymentViewSet class, which is responsible for
handling HTTP requests related to customer payment summaries.
"""

from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from authentication import get_authentication_classes
from base.views import ListView

from utils.swagger import (
    responses_400,
    responses_401,
    responses_404,
    responses_400_example,
    responses_401_example,
    responses_404_example,
)

from customer.db_access import customer_manager
from invoice.db_models.invoice import Invoice
from customer.db_models.customer import Customer

from ..serializers import (
    PaymentListResponseSerializer,
    Payment_list_success_example,
)

MODULE_NAME = "Payment"


class PaymentViewSet(ListView, viewsets.ViewSet):
    """
    ViewSet to return payment summary for all customers.
    """

    authentication_classes = get_authentication_classes()
    is_pagination = False
    list_serializer_class = None
    manager = customer_manager

    @extend_schema(
        responses={
            200: PaymentListResponseSerializer,
            **responses_400,
            **responses_401,
            **responses_404,
        },
        examples=[
            Payment_list_success_example,
            responses_400_example,
            responses_401_example,
            responses_404_example,
        ],
        tags=[MODULE_NAME],
    )
    def list_all(self, request, *args, **kwargs):
        """List all customers with their payment summaries."""
        return super().list_all(request, *args, **kwargs)

    def get_list(self, objects, request=None):
        customers = Customer.objects.all()

        result = []
        for customer in customers:
            invoices = Invoice.objects.filter(customer=customer)

            total = sum(inv.total for inv in invoices)
            paid = sum(inv.total for inv in invoices if inv.status == "PAID")
            pending = total - paid

            result.append(
                {
                    "customer_id": customer.customer_id,
                    "full_name": customer.get_full_name,
                    "total_amount": total,
                    "paid_amount": paid,
                    "pending_amount": pending,
                }
            )

        return result
