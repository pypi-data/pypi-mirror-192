from enum import Enum


class CardCardActivityResponseType(str, Enum):
    SETTLEMENT = "SETTLEMENT"
    REFUND = "REFUND"
    AUTHORISATION = "AUTHORISATION"
    REVERSAL = "REVERSAL"

    def __str__(self) -> str:
        return str(self.value)
