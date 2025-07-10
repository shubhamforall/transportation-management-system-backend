from rest_framework import serializers
from base.serializers.query import QuerySerializer

from customer.constants import CustomerTypeChoices
from invoice.constants import InvoiceStatusChoices


class InvoiceQuerySerializer(QuerySerializer):
    """
    Serializer for querying invoice instances.
    Inherits from QuerySerializer to handle common query parameters.
    """

    date = serializers.DateField()
    status = serializers.ChoiceField(
        choices=InvoiceStatusChoices.choices,
    )
    customer_type = serializers.ChoiceField(choices=CustomerTypeChoices.choices)
    company_name = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    vehicle_name = serializers.CharField(max_length=50)
    vehicle_type = serializers.CharField(max_length=50)
    vehicle_number = serializers.CharField(max_length=15)
