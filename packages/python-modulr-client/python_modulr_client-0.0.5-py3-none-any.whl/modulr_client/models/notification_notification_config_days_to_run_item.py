from enum import Enum


class NotificationNotificationConfigDaysToRunItem(str, Enum):
    TUESDAY = "TUESDAY"
    FRIDAY = "FRIDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    SATURDAY = "SATURDAY"
    MONDAY = "MONDAY"
    SUNDAY = "SUNDAY"

    def __str__(self) -> str:
        return str(self.value)
