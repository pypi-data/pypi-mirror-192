from enum import Enum


class GetPendingTransactionsByAccountTypeItem(str, Enum):
    PO_SWIFT = "PO_SWIFT"
    FE_ACMNT = "FE_ACMNT"
    PO_SEPA_INST = "PO_SEPA_INST"
    PI_BACS = "PI_BACS"
    ADHOC = "ADHOC"
    PO_REV = "PO_REV"
    FE_TXN = "FE_TXN"
    PI_SWIFT = "PI_SWIFT"
    PI_FAST = "PI_FAST"
    PO_SECT = "PO_SECT"
    PI_REV = "PI_REV"
    FE_ACOPN = "FE_ACOPN"
    PO_VISA = "PO_VISA"
    PI_BACS_CONTRA = "PI_BACS_CONTRA"
    PI_CHAPS = "PI_CHAPS"
    PI_MASTER = "PI_MASTER"
    PO_CHAPS = "PO_CHAPS"
    PI_DD = "PI_DD"
    PI_SEPA_INST = "PI_SEPA_INST"
    PO_REV_MASTER = "PO_REV_MASTER"
    FE_REV = "FE_REV"
    PO_MASTER = "PO_MASTER"
    INT_INTRAC = "INT_INTRAC"
    PI_VISA = "PI_VISA"
    PI_SECT = "PI_SECT"
    PO_DD = "PO_DD"
    PO_FAST = "PO_FAST"
    PI_FAST_REV = "PI_FAST_REV"
    INT_INTERC = "INT_INTERC"

    def __str__(self) -> str:
        return str(self.value)
