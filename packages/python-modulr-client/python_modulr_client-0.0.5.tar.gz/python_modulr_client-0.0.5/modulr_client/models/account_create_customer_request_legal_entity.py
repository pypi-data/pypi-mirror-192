from enum import Enum


class AccountCreateCustomerRequestLegalEntity(str, Enum):
    IE = "IE"
    NL = "NL"
    GB = "GB"

    def __str__(self) -> str:
        return str(self.value)
