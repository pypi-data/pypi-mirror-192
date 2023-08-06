from enum import Enum


class GetCardActivitiesStatuses(str, Enum):
    EXPIRED = "EXPIRED"
    SETTLED = "SETTLED"
    DECLINED = "DECLINED"
    APPROVED = "APPROVED"

    def __str__(self) -> str:
        return str(self.value)
