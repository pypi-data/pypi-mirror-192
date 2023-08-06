from enum import Enum


class PaymentBatchPaymentStatusesItem(str, Enum):
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"
    CANCELLED = "CANCELLED"
    ACCEPTED = "ACCEPTED"

    def __str__(self) -> str:
        return str(self.value)
