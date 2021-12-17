from TAInformation.Models.account_type import AccountType
from TAInformation.Models.validator_methods import *
from TAInformation.models import Course, User, LabCourseJunction, Lab


class UserAdmin(BaseUser):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        super().__init__(id_number, name, password, email, address, phone)
        self.role = AccountType.ADMIN

    # precondition: none
    # post condition: return an array of all ClassCourses course information
    def display_courses(self):
        all_courses = Course.objects.all()
        course_content = []
        for course in all_courses:
            all_labs_ids = LabCourseJunction.objects.filter(course_id=course.course_id)
            labs_string = ""
            for i in all_labs_ids:
                labs_string += " " + i.lab_id.lab_name
            course_information = [
                course.course_name,
                course.instructor_id.name,
                labs_string,
                course.meeting_time,
                course.semester,
                course.course_type,
                course.description,
            ]
            course_content.append(course_information)
        return course_content

    # precondition: none
    # post condition: return a String array of all people and their public and private info
    def display_people(self):
        all_users = User.objects.all()
        user_content = []
        for my_user in all_users:
            user_information = [
                my_user.name,
                my_user.password,
                my_user.email,
                my_user.home_address,
                AccountType(my_user.role).__str__(),
                my_user.phone
            ]
            user_content.append(user_information)
        return user_content

    def display_people_fields(self):
        return ["name", "password", "email", "home address", "role", "phone"]

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

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new id, if validation succeeds and id doesn't belong to another user
    def edit_user_id(self, user_to_edit: User, new_user_id: int):
        pass

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new name, if validation succeeds
    def edit_name(self, user_to_edit: User, new_name: str):
        pass

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new email, if validation succeeds and email doesn't belong to another
    # user
    def edit_email(self, user_to_edit: User, new_email: str):
        pass

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new password, if validation succeeds
    def edit_password(self, user_to_edit: User, new_password: str):
        pass

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new home address, if validation succeeds
    def edit_home_address(self, user_to_edit: User, new_address: str):
        pass

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new phone number, if validation succeeds
    def edit_phone(self, user_to_edit: User, new_phone: str):
        pass

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new role, if validation succeeds
    def edit_role(self, user_to_edit: User, new_role: AccountType):
        pass

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: 1) Record in User table is updated with new skill, if validation succeeds
    #       2) skill is added to Skills table, if no other existing user has the skill
    def add_skill(self, user_to_edit: User, new_skill: str):
        pass

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: 1) Record in User table is updated with lost_skill removed, if user has the skill
    #       2) skill is removed from Skills table, if no other existing user has the skill
    def remove_skill(self, user_to_edit: User, lost_skill: str):
        pass
