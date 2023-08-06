from enum import Enum


class CardsimulatorCardAuthorisationResponseStatus(str, Enum):
    REVERSED = "REVERSED"
    SETTLED = "SETTLED"
    APPROVED = "APPROVED"

    def __str__(self) -> str:
        return str(self.value)
