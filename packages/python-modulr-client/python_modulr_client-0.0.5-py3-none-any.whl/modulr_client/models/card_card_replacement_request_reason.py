from enum import Enum


class CardCardReplacementRequestReason(str, Enum):
    LOST = "LOST"
    STOLEN = "STOLEN"
    DAMAGED = "DAMAGED"
    RENEW = "RENEW"

    def __str__(self) -> str:
        return str(self.value)
