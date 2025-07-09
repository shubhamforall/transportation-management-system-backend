from base.db_access import manager
from ..db_models import Vehicle

class VehicleManager(manager.Manager[Vehicle]):
    """
    Manager class for the Vehicle model.
    """
    model = Vehicle
    
vehicle_manager = VehicleManager()