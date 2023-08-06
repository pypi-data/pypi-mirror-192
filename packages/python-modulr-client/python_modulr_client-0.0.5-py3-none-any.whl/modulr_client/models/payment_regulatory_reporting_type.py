from enum import Enum


class PaymentRegulatoryReportingType(str, Enum):
    DEBT = "DEBT"
    CRED = "CRED"
    BOTH = "BOTH"

    def __str__(self) -> str:
        return str(self.value)
