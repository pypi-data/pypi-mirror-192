from enum import Enum


class RuleCreateRuleRequestType(str, Enum):
    SWEEP = "SWEEP"
    FUNDING = "FUNDING"
    SPLIT = "SPLIT"

    def __str__(self) -> str:
        return str(self.value)
