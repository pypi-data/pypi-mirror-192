from enum import Enum


class CardCancelCardRequestReason(str, Enum):
    LOST = "LOST"
    STOLEN = "STOLEN"
    DESTROYED = "DESTROYED"

    def __str__(self) -> str:
        return str(self.value)
