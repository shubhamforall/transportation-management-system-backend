class PaymentStatus:
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"

    CHOICES = [
        (PENDING, "Pending"),
        (PAID, "Paid"),
        (FAILED, "Failed"),
    ]
