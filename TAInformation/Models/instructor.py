from TAInformation.Models.account_type import AccountType
from TAInformation.Models.base_user import BaseUser


class Instructor(BaseUser):
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        self.user_id = id_number
        self.name = name
        self.password = password
        self.email = email
        self.home_address = address
        self.phone_number = phone
        self.role = AccountType.INSTRUCTOR

    def display_courses(self):
        pass

    def display_people(self):
        pass

    def display_people_fields(self):
        pass

    def create_admin(self, new_admin):
        return {'result': False, 'errorMsg': "Only admins can create new users\n"}

    def create_instructor(self, new_instructor):
        return self.create_admin(new_instructor)

    def create_ta(self, new_ta):
        return self.create_admin(new_ta)