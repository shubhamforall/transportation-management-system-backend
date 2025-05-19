from rest_framework import viewsets
from authentication import get_authentication_classes   

from base.views import BaseView

from ..db_access.invoice import invoice_manager
from ..serializers.invoice import InvoiceSerializer

class InvoiceViewSet(BaseView, viewsets.ViewSet):
    """
    ViewSet for handling invoice endpoints.
    """

    authentication_classes = get_authentication_classes()
    manager = invoice_manager
    serializer_class = InvoiceSerializer
    lookup_field = "invoice_id"