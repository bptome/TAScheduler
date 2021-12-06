
from TAInformation.Models.base_user import BaseUser
from TAInformation.Models.account_type import AccountType


class UserAdmin(BaseUser):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        super().__init__(id_number, name, password, email, address, phone)
        self.role = AccountType.ADMIN

    # precondition: none
    # post condition: return an array of all Courses
    def display_courses(self):
        return []

    # precondition: none
    # post condition: return a String array of all people and their public and private info
    def display_people(self):
        return []

    def display_people_fields(self):
        return []

    def create_admin(self, new_admin: BaseUser):
        if new_admin.role != AccountType.ADMIN:
            return False

    def __create_user_validator(self, new_admin: BaseUser):
        pass





