from rest_framework import viewsets
from authentication import get_authentication_classes

from base.views import BaseView

from ..db_access.vehicle import vehicle_manager
from ..serializers.vehicle import VehicleSerializer

class VehicleViewSet(BaseView, viewsets.ViewSet):
    """
    ViewSet for handling vehicle endpoints.
    """

    authentication_classes = get_authentication_classes()
    manager = vehicle_manager
    serializer_class = VehicleSerializer
    lookup_field = "vehicle_id"