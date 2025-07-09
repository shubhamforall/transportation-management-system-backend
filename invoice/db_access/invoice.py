from base.db_access import manager
from ..db_models.invoice import Invoice

class InvoiceManager(manager.Manager[Invoice]):
    """
    Manager class for the Invoice model.
    """
    model = Invoice

invoice_manager = InvoiceManager()