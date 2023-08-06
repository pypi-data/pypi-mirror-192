from enum import Enum


class CardAsyncTaskResponseStatus(str, Enum):
    ERROR = "ERROR"
    RECEIVED = "RECEIVED"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"

    def __str__(self) -> str:
        return str(self.value)
