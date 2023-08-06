from enum import Enum


class InboundpaymentInboundPaymentRequestType(str, Enum):
    PO_REV = "PO_REV"
    PI_CHAPS = "PI_CHAPS"
    PI_SEPA_INST = "PI_SEPA_INST"
    PI_FAST = "PI_FAST"
    PI_BACS = "PI_BACS"
    PI_SECT = "PI_SECT"
    PI_DD = "PI_DD"
    PI_FP = "PI_FP"
    INT_INTERC = "INT_INTERC"

    def __str__(self) -> str:
        return str(self.value)
