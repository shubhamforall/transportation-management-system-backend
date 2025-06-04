from django.db import models


class InvoiceStatusChoices(models.TextChoices):
    """
    Enum for invoice status.
    """

    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"
