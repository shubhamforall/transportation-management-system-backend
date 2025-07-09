from rest_framework import viewsets
from authentication import get_authentication_classes
from base.views import ListView

from invoice.db_models.invoice import Invoice
from customer.db_models.customer import Customer
from customer.db_access import customer_manager


class PaymentViewSet(ListView, viewsets.ViewSet):
    """
    ViewSet to return payment summary for all customers.
    """

    authentication_classes = get_authentication_classes()
    is_pagination = False
    list_serializer_class = None
    manager = customer_manager

    def get_list(self, objects, request=None):
        # Get all customers from DB
        customers = Customer.objects.all()

        result = []
        for customer in customers:
            invoices = Invoice.objects.filter(customer=customer)

            total = sum(inv.total for inv in invoices)
            paid = sum(inv.total for inv in invoices if inv.status == "PAID")
            pending = total - paid

            result.append({
                "customer_id": customer.customer_id,
                "full_name": customer.get_full_name,
                "total_amount": total,
                "paid_amount": paid,
                "pending_amount": pending,
            })

        return result
