from enum import Enum


class AccountCustomerType(str, Enum):
    SOLETRADER = "SOLETRADER"
    CHARITY = "CHARITY"
    INDIVIDUAL = "INDIVIDUAL"
    PCM_BUSINESS = "PCM_BUSINESS"
    LPARTNRSHP = "LPARTNRSHP"
    TRUST = "TRUST"
    LLC = "LLC"
    PLC = "PLC"
    OPARTNRSHP = "OPARTNRSHP"
    LLP = "LLP"
    PCM_INDIVIDUAL = "PCM_INDIVIDUAL"

    def __str__(self) -> str:
        return str(self.value)
