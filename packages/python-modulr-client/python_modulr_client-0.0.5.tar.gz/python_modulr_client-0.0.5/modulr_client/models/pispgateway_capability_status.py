from enum import Enum


class PispgatewayCapabilityStatus(str, Enum):
    INACTIVE = "INACTIVE"
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"

    def __str__(self) -> str:
        return str(self.value)
