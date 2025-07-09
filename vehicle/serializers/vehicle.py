from rest_framework import serializers

from utils.messages import error
from utils.exceptions import codes

from ..db_access.vehicle import vehicle_manager

class VehicleSerializer(serializers.Serializer):
    """
    Serializer for both creating and updating a vehicle.
    """

    vehicle_name = serializers.CharField(required=True, max_length=50)
    vehicle_type = serializers.CharField(required=True, max_length=50)
    vehicle_number = serializers.CharField(required=True, max_length=15)
    vehicle_model = serializers.CharField(required=True, max_length=50)
    vehicle_color = serializers.CharField(required=True, max_length=50)

    def validate_vehicle_number(self, value):
        """
        Validate vehicle_number field.
        - For create: vehicle_number must not exist.
        - For update: vehicle_number must not belong to a different vehicle.
        """

        is_update = self.instance is not None

        query = {"vehicle_number": value}
        if is_update:
            query["vehicle_id"] = {"NOT": self.instance.vehicle_id}

        if vehicle_manager.exists(query=query):
            raise serializers.ValidationError(
                error.ALREADY_EXIST,
                code=codes.DUPLICATE_ENTRY,
            )

        return value