from enum import Enum


class AccountStatusesItem(str, Enum):
    CLIENT_BLOCKED = "CLIENT_BLOCKED"
    BLOCKED = "BLOCKED"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

    def __str__(self) -> str:
        return str(self.value)
