from django.db import models
from base.db_models.model import BaseModel

from utils.functions import get_uuid

from ..constants import InvoiceStatusChoices

class Invoice(BaseModel, models.Model):
    """
    Model to store invoice details linking customer and vehicle.
    """

    invoice_id = models.CharField(max_length=36, primary_key=True, default=get_uuid)
    customer = models.ForeignKey("customer.Customer", on_delete=models.CASCADE)
    vehicle = models.ForeignKey("vehicle.Vehicle", on_delete=models.CASCADE)
    date = models.DateField()
    loading_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=64, choices=InvoiceStatusChoices.choices)
    
    
    class Meta:
        db_table = "invoice"

    def to_dict(self):
        return {
            "invoice_id": self.invoice_id,
            "customer": self.customer.customer_id,
            "vehicle": self.vehicle.vehicle_id,
            "date": self.date,
            "loading_address": self.loading_address,
            "delivery_address": self.delivery_address,
            "weight": float(self.weight),
            "rate": float(self.rate),
            "total": float(self.total),
            "status": self.status,
        }
