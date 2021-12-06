from abc import ABC, abstractmethod
from TAInformation.Models.account_type import AccountType


class BaseUser(ABC):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        super().__init__(id_number, name, password, email, address, phone)
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
    # post: Returns a dict object with the result and message about result
    # side: Creates new admin if all data is valid and admin doesn't already exist
    def create_admin(self, new_admin):
        pass

    # pre: new_instructor is derived from type BaseUser
    # post: Returns a dict object with the result and message about result
    # side: Creates new instructor if all data is valid and instructor doesn't already exist
    @abstractmethod
    def create_instructor(self, new_instructor):
        pass

    # pre: new_ta is derived from type BaseUser
    # post: Returns a dict object with the result and message about result
    # side: Creates new TA if all data is valid and TA doesn't already exist
    @abstractmethod
    def create_ta(self, new_ta):
        pass

