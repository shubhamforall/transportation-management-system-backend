from django.dispatch import receiver
from django.db.models.signals import post_save

from base.db_access import manager
from notification.constants import NotificationTypes
from notification.helper import Notification


from ..db_models.invoice import Invoice
from ..constants import InvoiceNotificationMessages


class InvoiceManager(manager.Manager[Invoice]):
    """
    Manager class for the Invoice model.
    """

    model = Invoice


@receiver(post_save, sender=Invoice)
def send_notification_on_invoice_movement(sender, instance: Invoice, created, **__):
    """
    Signal receiver that sends a notification when a Invoice instance is created.
    """
    if not created:
        return

    created_by = getattr(instance, "created_by", None)
    if not created_by:
        return

    notification_data = {
        "date": instance.date.isoformat() if instance.date else None,
    }

    Notification(
        InvoiceNotificationMessages.TITLE,
        InvoiceNotificationMessages.MESSAGE,
        NotificationTypes.INVOICE,
        notification_data,
    ).send_notification([created_by])


invoice_manager = InvoiceManager()
