from enum import Enum


class GetCustomersNameType(str, Enum):
    WORD_MATCH = "WORD_MATCH"
    PREFIX = "PREFIX"
    WORD_MATCH_ALPHANUMERIC = "WORD_MATCH_ALPHANUMERIC"
    CONTAINS = "CONTAINS"
    SUFFIX = "SUFFIX"
    EXACT = "EXACT"

    def __str__(self) -> str:
        return str(self.value)
