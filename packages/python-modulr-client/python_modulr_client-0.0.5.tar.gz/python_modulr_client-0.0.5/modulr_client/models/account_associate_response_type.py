from enum import Enum


class AccountAssociateResponseType(str, Enum):
    SOLETRADER = "SOLETRADER"
    INDIVIDUAL = "INDIVIDUAL"
    PCM_INDIVIDUAL = "PCM_INDIVIDUAL"
    DIRECTOR = "DIRECTOR"
    PARTNER = "PARTNER"
    BENE_OWNER = "BENE_OWNER"
    TRUST_SETTLOR = "TRUST_SETTLOR"
    C_INTEREST = "C_INTEREST"
    TRUST_BENEFICIARY = "TRUST_BENEFICIARY"
    SIGNATORY = "SIGNATORY"
    TRUST_TRUSTEE = "TRUST_TRUSTEE"
    CSECRETARY = "CSECRETARY"

    def __str__(self) -> str:
        return str(self.value)
