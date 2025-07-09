from django.urls import path

from ..views.vehicle import VehicleViewSet

urlpatterns = [
    path(
        "vehicle",
        VehicleViewSet.as_view(VehicleViewSet.get_method_view_mapping()),
        name="vehicle",
    ),
    path(
        "vehicle/<str:vehicle_id>",
        VehicleViewSet.as_view(VehicleViewSet.get_method_view_mapping(True)),
        name="vehicle-detail",
    ),
]
