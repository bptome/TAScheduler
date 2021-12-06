from enum import Enum


class AccountType(Enum):
    DEFAULT = 0
    TA = 1
    INSTRUCTOR = 2
    ADMIN = 3

    # pre conditions: 0-3 enum value
    # post condition: returns a string associated with the enum value
    # side effects: raises an error if enum value is outside 0-3
    def __str__(self):
        if self.value == self.DEFAULT.value:
            return "Default"
        elif self.value == self.TA.value:
            return "TA"
        elif self.value == self.INSTRUCTOR.value:
            return "Instructor"
        elif self.value == self.ADMIN.value:
            return "Admin"
