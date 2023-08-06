from enum import Enum


class PaymentBatchPaymentStatus(str, Enum):
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"
    CANCELLED = "CANCELLED"
    ACCEPTED = "ACCEPTED"

    def __str__(self) -> str:
        return str(self.value)
