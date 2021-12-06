
from TAInformation.Models.base_user import BaseUser
from TAInformation.Models.account_type import AccountType
from TAInformation.Models.validator_methods import *
from TAInformation.models import User


class UserAdmin(BaseUser):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        self.user_id = id_number
        self.name = name
        self.password = password
        self.email = email
        self.home_address = address
        self.phone_number = phone
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
        return_dict = {}

        return_dict = name_validator(new_admin)
        error_msg = return_dict['errorMsg']

        return_dict = password_validator(new_admin)
        error_msg += return_dict['errorMsg']

        return_dict = email_validator(new_admin)
        error_msg += return_dict['errorMsg']

        return_dict = address_validator(new_admin)
        error_msg += return_dict['errorMsg']

        return_dict = phone_validator(new_admin)
        error_msg += return_dict['errorMsg']

        if error_msg != "":
            return {'result': False, 'message': error_msg}

        # Data is at least valid at this point
        user_exists = User.objects.filter(email=new_admin.email).exists()

        if user_exists:
            return {'result': False, 'message': "User already exists"}

        # User is indeed new user at this point
        self._save_new_user(new_admin)
        return {'result': True, 'message': "New admin has been created"}


    def create_instructor(self, new_instructor: BaseUser):
        pass

    def create_ta(self, new_ta: BaseUser):
        pass

    def _save_new_user(self, new_user: BaseUser):
        pass



