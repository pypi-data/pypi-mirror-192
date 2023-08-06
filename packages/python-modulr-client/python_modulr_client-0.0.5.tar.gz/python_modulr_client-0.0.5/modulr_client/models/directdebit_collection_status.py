from enum import Enum


class DirectdebitCollectionStatus(str, Enum):
    CANCELLED = "CANCELLED"
    SCHEDULED = "SCHEDULED"
    REPRESENTABLE = "REPRESENTABLE"
    SUCCESS = "SUCCESS"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    REPRESENTED = "REPRESENTED"

    def __str__(self) -> str:
        return str(self.value)
