from rest_framework import viewsets
from authentication import get_authentication_classes

from base.views import BaseView

from ..db_access.customer import customer_manager
from ..serializers.customer import CustomerSerializer

class CustomerViewSet(BaseView, viewsets.ViewSet):
    """
    ViewSet for handling customer endpoints.
    """

    authentication_classes = get_authentication_classes()
    manager = customer_manager
    serializer_class = CustomerSerializer
    lookup_field = "customer_id"