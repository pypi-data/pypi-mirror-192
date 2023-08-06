from enum import Enum


class GetCreatePhysicalCardAsyncTasksByAccountStatuses(str, Enum):
    ERROR = "ERROR"
    RECEIVED = "RECEIVED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"

    def __str__(self) -> str:
        return str(self.value)
