from TAInformation.Models.account_type import AccountType
from TAInformation.Models.base_user import BaseUser
from TAInformation.models import User


class TA(BaseUser):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        super().__init__(id_number, name, password, email, address, phone)
        self.role = AccountType.TA

    def display_courses(self):
        pass

    def display_people(self):
        pass

    def display_people_fields(self):
        pass

    # pre: None
    # post: Returns dict object with message of inability to create accounts
    def create_user(self, new_user):
        return {'result': False, 'message': "Only admins can create new users\n"}

    # pre: None
    # post: Returns a dict object with the result and message about inability to edit their user id
    # side: None
    def edit_user_id(self, user_to_edit: User, new_user_id: int):
        pass

    # pre: None
    # post: Returns a dict object with the result and message about inability to edit their name
    # side: None
    def edit_name(self, user_to_edit: User, new_name: str):
        pass

    # pre: None
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new email, if validation succeeds and email doesn't belong to another
    # user
    def edit_email(self, user_to_edit: User, new_email: str):
        pass

    # pre: None
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new password, if validation succeeds
    def edit_password(self, user_to_edit: User, new_password: str):
        pass

    # pre: None
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new home address, if validation succeeds
    def edit_home_address(self, user_to_edit: User, new_address: str):
        pass

    # pre: None
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new phone number, if validation succeeds
    def edit_phone(self, user_to_edit: User, new_phone: str):
        pass

    # pre: None
    # post: Returns a dict object with the result and message about inability to edit role
    # side: None
    def edit_role(self, user_to_edit: User, new_role: AccountType):
        pass

    # pre: Calling user is in the database
    # post: Returns a QueryList of all users that can be edited by calling user
    # side: None
    def list_of_editable_users(self) -> list[User]:
        pass

    # pre: None
    # post: Returns a dict object with the result and message about result
    # side: 1) Record in User table is updated with new skill, if validation succeeds
    #       2) skill is added to Skills table, if no other existing user has the skill
    def add_skill(self, user_to_edit: User, new_skill: str):
        pass

    # pre: None
    # post: Returns a dict object with the result and message about result
    # side: 1) Record in User table is updated with lost_skill removed, if user has the skill
    #       2) skill is removed from Skills table, if no other existing user has the skill
    def remove_skill(self, user_to_edit: User, lost_skill: str):
        pass

    # pre: user_to_view is a User model object
    # post: Returns a dict object with a message and list of skills, if access to view is granted
    # side: None
    def list_skills(self, user_to_view: User):
        pass
