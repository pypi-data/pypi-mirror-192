from enum import Enum


class AccountAccessGroupWithDetailsResponseStatus(str, Enum):
    DELETED = "DELETED"
    ACTIVE = "ACTIVE"

    def __str__(self) -> str:
        return str(self.value)
