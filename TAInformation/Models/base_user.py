from abc import ABC, abstractmethod
from curses.ascii import isupper, islower, isdigit

from TAInformation.Models.account_type import AccountType


# Data validating methods
# For all methods:
# Pre: Argument passed is derived from BaseUser
# Post: Returns dict object that indicates result of validation and error message, if needed

# Start of data validation methods
def id_validator(new_user):
    if new_user.user_id is None or new_user.user_id < 0:
        return {'result': False, 'errorMsg': "Invalid user id name entered\n"}

    return {'result': True, 'errorMsg': ""}


def name_validator(new_user):
    if new_user.name is None or len(new_user.name) < 5:
        return {'result': False, 'errorMsg': "Invalid name given\n"}

    return {'result': True, 'errorMsg': ""}


def password_validator(new_user):
    if new_user.password is None or len(new_user.password) < 4:
        return {'result': True, 'errorMsg': "Password must be at least 4 characters long\n"}

    uppercase_missing = True
    lowercase_missing = True
    number_missing = True
    special_char_missing = True

    # Loop to check if password format is correct
    for c in new_user.password:
        if isupper(c):
            uppercase_missing = False
        elif islower(c):
            lowercase_missing = False
        elif isdigit(c):
            number_missing = False
        else:
            special_char_missing = False

    error_msg = ""
    if uppercase_missing:
        error_msg += "Password must contain >= 1 uppercase letter\n"

    if lowercase_missing:
        error_msg += "Password must contain >= 1 lowercase letter\n"

    if number_missing:
        error_msg += "Password must contain >= 1 number\n"

    if special_char_missing:
        error_msg += "Password must contain >= 1 non-alphanumeric character\n"

    if error_msg != "":
        return {'result': False, 'errorMsg': error_msg}

    return {'result': True, 'errorMsg': ""}


# End of data validation methods

class BaseUser(ABC):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        self.user_id = id_number
        self.name = name
        self.password = password
        self.email = email
        self.home_address = address
        self.phone_number = phone
        self.role = AccountType.DEFAULT

    # precondition: none
    # post condition: return an array of Course specific to the user
    @abstractmethod
    def display_courses(self):
        pass

    # precondition: none
    # post condition: return an array of User
    @abstractmethod
    def display_people(self):
        pass

    # precondition: none
    # post condition: return an array of User
    @abstractmethod
    def display_people_fields(self):
        pass

    # pre: new_admin is derived from type BaseUser
    # post: Creates new admin if all data is valid and admin doesn't already exist
    @abstractmethod
    def create_admin(self, new_admin):
        pass
