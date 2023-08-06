from enum import Enum


class DirectdebitCollectionScheduleResponseStatus(str, Enum):
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    SUBMITTED = "SUBMITTED"
    REJECTED = "REJECTED"
    ACTIVE = "ACTIVE"

    def __str__(self) -> str:
        return str(self.value)
