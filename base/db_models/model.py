"""
Base model
"""

from django.db import models


class BaseModel(models.Model):
    """
    Base abstract model which is having the common field.
    """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created_by = models.CharField(max_length=128)
    updated_by = models.CharField(max_length=128)

    updated_dtm = models.DateTimeField(auto_now=True)
    created_dtm = models.DateTimeField(auto_now_add=True)
    deleted_dtm = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True
