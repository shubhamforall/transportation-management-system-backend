"""
Invoice constants module.
"""

from django.db import models


class CustomerTypeChoices(models.TextChoices):
    """
    Enum for customer.
    """

    BUSINESS = "BUSINESS", "Business"
    INDIVIDUAL = "INDIVIDUAL", "Individual"

