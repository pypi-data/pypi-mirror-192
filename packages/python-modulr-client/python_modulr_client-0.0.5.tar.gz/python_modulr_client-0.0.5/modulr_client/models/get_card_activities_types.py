from enum import Enum


class GetCardActivitiesTypes(str, Enum):
    SETTLEMENT = "SETTLEMENT"
    REFUND = "REFUND"
    AUTHORISATION = "AUTHORISATION"
    REVERSAL = "REVERSAL"

    def __str__(self) -> str:
        return str(self.value)
