from enum import Enum


class DirectdebitMandateStatus(str, Enum):
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    SUBMITTED = "SUBMITTED"
    SUSPENDED = "SUSPENDED"
    REJECTED = "REJECTED"
    ACTIVE = "ACTIVE"

    def __str__(self) -> str:
        return str(self.value)
