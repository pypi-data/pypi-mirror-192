from enum import Enum


class DirectdebitCreateCollectionScheduleRequestFrequency(str, Enum):
    ONCE = "ONCE"
    EVERY_FOUR_WEEKS = "EVERY_FOUR_WEEKS"
    SEMI_ANNUALLY = "SEMI_ANNUALLY"
    ANNUALLY = "ANNUALLY"
    WEEKLY = "WEEKLY"
    QUARTERLY = "QUARTERLY"
    MONTHLY = "MONTHLY"
    EVERY_TWO_WEEKS = "EVERY_TWO_WEEKS"

    def __str__(self) -> str:
        return str(self.value)
