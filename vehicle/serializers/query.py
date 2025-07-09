from rest_framework import serializers
from base.serializers.query import QuerySerializer


class VehicleQuerySerializer(QuerySerializer):
    """
    Serializer for querying vehicles.
    """

    vehicle_name = serializers.CharField(max_length=50)
    vehicle_type = serializers.CharField(max_length=50)
    vehicle_number = serializers.CharField(max_length=15)
    vehicle_model = serializers.CharField(max_length=50)
    vehicle_color = serializers.CharField(max_length=50)
