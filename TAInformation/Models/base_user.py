from abc import ABC, abstractmethod
from TAInformation.Models.account_type import AccountType


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

