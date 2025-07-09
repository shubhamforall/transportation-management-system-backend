from django.urls import path

from invoice.views import InvoiceViewSet

urlpatterns = [
    path(
        "invoice",
        InvoiceViewSet.as_view(InvoiceViewSet.get_method_view_mapping()),
        name="invoice",
    ),
    path(
        "invoice/<str:invoice_id>",
        InvoiceViewSet.as_view(InvoiceViewSet.get_method_view_mapping(True)),
        name="invoice-detail",
    ),
]