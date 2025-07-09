from django.db import models
from base.db_models.model import BaseModel
from utils.functions import get_uuid

class Vehicle(BaseModel, models.Model):
    """
    Model to save vehicle information.
    """

    vehicle_id = models.CharField(
        max_length=36,
        primary_key=True,
        default=get_uuid,
    )
    vehicle_name = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=15, unique=True)
    vehicle_model= models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=50)

    class Meta:
        """
        db_table (str): Specifies the database table name for the model.
        """

        db_table = "vehicle"
        
    def to_dict(self):
        """
        Convert the Vehicle instance to a dictionary representation.

        Returns:
            dict: Dictionary representation of the Vehicle instance.
        """
        return {
            "vehicle_id": self.vehicle_id,
            "vehicle_name": self.vehicle_name,
            "vehicle_type": self.vehicle_type,
            "vehicle_number": self.vehicle_number,
            "vehicle_model": self.vehicle_model,
            "vehicle_color": self.vehicle_color,
        }