from enum import Enum


class PaymentfileuploadFileCreatePaymentsResponseStatus(str, Enum):
    DUPLICATE = "DUPLICATE"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    PROCESSED = "PROCESSED"
    VALID = "VALID"
    REJECTED = "REJECTED"
    INVALID = "INVALID"

    def __str__(self) -> str:
        return str(self.value)
