""" 
Customer model for invoice management.
Contains configurations unique to customer module.
"""
from django.db import models
from base.db_models.model import BaseModel
from utils.functions import get_uuid


class Customer(BaseModel, models.Model):
    """
    Model to save customer information.
    """

    customer_id = models.CharField(
        max_length=36,
        primary_key=True,
        default=get_uuid,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True)
    address = models.CharField(max_length=255)

    class Meta:
        """
        db_table (str): Specifies the database table name for the model.
        """

        db_table = "customer"
        
    @property
    def get_full_name(self):
        """
        Returns the full name of the customer.

        Returns:
            str: Full name of the customer.
        """
        return f"{self.first_name} {self.last_name}".title()

    def to_dict(self):
        """
        Convert the Customer instance to a dictionary representation.

        Returns:
            dict: Dictionary representation of the Customer instance.
        """
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name,
            "mobile_number": self.mobile_number,
            "email": self.email,
            "address": self.address,
        }
