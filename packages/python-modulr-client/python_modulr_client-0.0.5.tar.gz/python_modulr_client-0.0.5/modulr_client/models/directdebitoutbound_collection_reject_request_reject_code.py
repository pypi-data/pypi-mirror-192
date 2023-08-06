from enum import Enum


class DirectdebitoutboundCollectionRejectRequestRejectCode(str, Enum):
    PRESENTATION_OVERDUE = "PRESENTATION_OVERDUE"
    AMOUNT_NOT_YET_DUE = "AMOUNT_NOT_YET_DUE"
    AMOUNT_DIFFERS = "AMOUNT_DIFFERS"
    SKIP_DEBIT_ATTEMPT = "SKIP_DEBIT_ATTEMPT"
    ADVANCE_NOTICE_DISPUTED = "ADVANCE_NOTICE_DISPUTED"

    def __str__(self) -> str:
        return str(self.value)
