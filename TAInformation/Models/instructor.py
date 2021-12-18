from TAInformation.Models.account_type import AccountType
from TAInformation.Models.base_user import BaseUser


class Instructor(BaseUser):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        super().__init__(id_number, name, password, email, address, phone)
        self.role = AccountType.INSTRUCTOR

    def display_courses(self):
        pass

    def display_people(self):
        pass

    def display_people_fields(self):
        pass
