from enum import Enum


class GetAccessGroupsStatusesItem(str, Enum):
    DELETED = "DELETED"
    ACTIVE = "ACTIVE"

    def __str__(self) -> str:
        return str(self.value)
