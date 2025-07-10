from django.db import models


class InvoiceStatusChoices(models.TextChoices):
    """
    Enum for invoice status.
    """

    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"


class InvoiceNotificationMessages(models.TextChoices):
    """
    Notification titles and messages for the Invoice module.
    """

    TITLE = "Invoice notification", "Invoice notification"
    MESSAGE = "Invoice created successfully", "Invoice created successfully"
