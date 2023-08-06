from enum import Enum


class AccountIdentifierCountrySpecificDetailsResponseBankCodeType(str, Enum):
    CHIPS = "CHIPS"
    ABA = "ABA"

    def __str__(self) -> str:
        return str(self.value)
