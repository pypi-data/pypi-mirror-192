from enum import Enum


class GetCardsByAccountStatuses(str, Enum):
    CANCELLED = "CANCELLED"
    CREATED = "CREATED"
    SUSPENDED = "SUSPENDED"
    EXPIRED = "EXPIRED"
    BLOCKED = "BLOCKED"
    ACTIVE = "ACTIVE"

    def __str__(self) -> str:
        return str(self.value)
