"""
Notification constants module.
"""

from django.db import models


class NotificationTypes(models.TextChoices):
    """
    Enum for notification types.
    """

    INVOICE = "INVOICE", "Invoice"
    PAYMENT = "PAYMENT", "Payment"
