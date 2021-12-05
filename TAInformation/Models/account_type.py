from enum import Enum


class AccountType(Enum):
    DEFAULT = 0
    TA = 1
    INSTRUCTOR = 2
    ADMIN = 3

    def __str__(self):
        if self.value == self.ADMIN.value:
            return "Admin"
        elif self.value == self.TA.value:
            return "TA"
        elif self.value == self.INSTRUCTOR.value:
            return "Instructor"
        else:
            return "Default"
