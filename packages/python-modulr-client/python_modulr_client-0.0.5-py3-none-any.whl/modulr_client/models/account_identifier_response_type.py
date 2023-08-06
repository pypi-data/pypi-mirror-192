from enum import Enum


class AccountIdentifierResponseType(str, Enum):
    INTL = "INTL"
    SCAN = "SCAN"
    DD = "DD"
    IBAN = "IBAN"

    def __str__(self) -> str:
        return str(self.value)
