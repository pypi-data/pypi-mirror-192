from enum import Enum


class InboundpaymentAccountIdentifierDetailRequestType(str, Enum):
    INTL = "INTL"
    SCAN = "SCAN"
    DD = "DD"
    IBAN = "IBAN"

    def __str__(self) -> str:
        return str(self.value)
