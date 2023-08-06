from enum import Enum


class PaymentDestinationType(str, Enum):
    SCAN = "SCAN"
    BENEFICIARY = "BENEFICIARY"
    IBAN = "IBAN"
    ACCOUNT = "ACCOUNT"

    def __str__(self) -> str:
        return str(self.value)
