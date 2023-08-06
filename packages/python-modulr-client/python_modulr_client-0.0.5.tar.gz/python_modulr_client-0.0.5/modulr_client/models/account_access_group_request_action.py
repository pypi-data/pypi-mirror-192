from enum import Enum


class AccountAccessGroupRequestAction(str, Enum):
    REMOVE = "REMOVE"
    ADD = "ADD"

    def __str__(self) -> str:
        return str(self.value)
