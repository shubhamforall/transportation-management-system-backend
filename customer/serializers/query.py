from rest_framework import serializers
from base.serializers.query import QuerySerializer

from customer.constants import CustomerTypeChoices


class CustomerQuerySerializer(QuerySerializer):

    customer_type = serializers.ChoiceField(choices=CustomerTypeChoices.choices)
    company_name = serializers.CharField(
        max_length=100,
        required=False,
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
