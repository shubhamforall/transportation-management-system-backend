from django.urls import path

from customer.views import CustomerViewSet

urlpatterns = [
    path(
        "customer",
        CustomerViewSet.as_view(CustomerViewSet.get_method_view_mapping()),
        name="customer",
    ),
    path(
        "customer/<str:customer_id>",
        CustomerViewSet.as_view(CustomerViewSet.get_method_view_mapping(True)),
        name="customer-detail",
    ),
]