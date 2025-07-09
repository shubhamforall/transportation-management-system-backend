""" 
This module imports the Customer class from the customer module
and makes it available for use in other parts of the application.
"""
from ..db_models.customer import Customer

_all__ = ["Customer"]