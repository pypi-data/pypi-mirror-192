from enum import Enum


class PaymentPaymentResponseApprovalStatus(str, Enum):
    PENDING = "PENDING"
    NOTNEEDED = "NOTNEEDED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DELETED = "DELETED"

    def __str__(self) -> str:
        return str(self.value)
