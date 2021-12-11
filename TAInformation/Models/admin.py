
from TAInformation.Models.base_user import BaseUser
from TAInformation.Models.account_type import AccountType
from TAInformation.Models.validator_methods import *
from TAInformation.models import User


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

    def create_user(self, user_to_add: BaseUser):
        error_msg = build_error_message(user_to_add)

        if error_msg != "":
            return {'result': False, 'message': error_msg}

        # Data is at least valid at this point
        user_exists = User.objects.filter(email=user_to_add.email).exists()
        user_exists = user_exists or User.objects.filter(user_id=user_to_add.user_id).exists()

        if user_exists:
            return {'result': False, 'message': "User already exists"}

        # User is indeed new user at this point
        save_new_user(user_to_add)
        success_msg = "New " + user_to_add.role.name + " has been created"
        return {'result': True, 'message': success_msg}






