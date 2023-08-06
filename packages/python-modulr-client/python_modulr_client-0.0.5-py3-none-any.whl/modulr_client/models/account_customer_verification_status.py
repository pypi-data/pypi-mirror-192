from enum import Enum


class AccountCustomerVerificationStatus(str, Enum):
    DECLINED = "DECLINED"
    VERIFIED = "VERIFIED"
    MIGRATED = "MIGRATED"
    REVIEWED = "REVIEWED"
    EXVERIFIED = "EXVERIFIED"
    REFERRED = "REFERRED"
    UNVERIFIED = "UNVERIFIED"

    def __str__(self) -> str:
        return str(self.value)
