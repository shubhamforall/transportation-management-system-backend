from base.db_access import manager
from ..db_models import Customer

class CustomerManager(manager.Manager[Customer]):
    """
    Manager class for the Customer model.
    """
    model = Customer
    
customer_manager = CustomerManager()