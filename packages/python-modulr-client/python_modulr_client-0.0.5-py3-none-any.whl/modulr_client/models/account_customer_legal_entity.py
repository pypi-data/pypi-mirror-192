from enum import Enum


class AccountCustomerLegalEntity(str, Enum):
    IE = "IE"
    NL = "NL"
    GB = "GB"

    def __str__(self) -> str:
        return str(self.value)
