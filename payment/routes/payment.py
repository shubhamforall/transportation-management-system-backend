from django.urls import path

from payment.views import PaymentViewSet
urlpatterns = [
    path(
        "payment",
        PaymentViewSet.as_view(PaymentViewSet.get_method_view_mapping()),
        name="payment",
    ),
]
