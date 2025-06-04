from rest_framework import viewsets
from authentication import get_authentication_classes   

from base.views import BaseView
from ..db_access.invoice import invoice_manager
from ..serializers.invoice import InvoiceSerializer

from customer.db_access import customer_manager
from vehicle.db_access import vehicle_manager

class InvoiceViewSet(BaseView, viewsets.ViewSet):
    """
    ViewSet for handling invoice endpoints.
    """

    authentication_classes = get_authentication_classes()
    manager = invoice_manager
    serializer_class = InvoiceSerializer
    lookup_field = "invoice_id"

    def get_list(self, objects, request=None):
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
