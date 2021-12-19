from django.db.models import F
from django.db.models.functions import Lower

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
        current_id = user_to_edit.user_id
        user_to_edit.user_id = new_user_id
        validation_result = id_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.user_id = current_id
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        if User.objects.filter(user_id=user_to_edit.user_id).exists():
            user_to_edit.user_id = current_id
            return {'result': False, 'message': "User with given ID already exists\n"}

        user_to_edit.save()
        success_msg = "The " + AccountType(
            user_to_edit.role).__str__() + ", " + user_to_edit.name + ", now has the ID # "
        success_msg += str(user_to_edit.user_id) + "\n"
        return {'result': True, 'message': success_msg}

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new name, if validation succeeds
    def edit_name(self, user_to_edit: User, new_name: str):
        current_name = user_to_edit.name
        user_to_edit.name = new_name
        validation_result = name_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.name = current_name
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        user_to_edit.save()
        success_msg = "The " + AccountType(
            user_to_edit.role).__str__() + " formerly known as " + current_name + " is now "
        success_msg += user_to_edit.name + "\n"
        return {'result': True, 'message': success_msg}

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new email, if validation succeeds and email doesn't belong to another
    # user
    def edit_email(self, user_to_edit: User, new_email: str):
        current_email = user_to_edit.email
        user_to_edit.email = new_email
        validation_result = email_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.email = current_email
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        if User.objects.filter(email=user_to_edit.email).exists():
            user_to_edit.email = current_email
            return {'result': False, 'message': "User with given email already exists\n"}

        user_to_edit.save()
        success_msg = "The email for " + user_to_edit.name + " is now " + user_to_edit.email + "\n"
        return {'result': True, 'message': success_msg}

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new password, if validation succeeds
    def edit_password(self, user_to_edit: User, new_password: str):
        current_password = user_to_edit.password
        user_to_edit.password = new_password
        validation_result = password_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.password = current_password
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        user_to_edit.save()
        success_msg = user_to_edit.name + "\'s password has been successfully changed\n"
        return {'result': True, 'message': success_msg}

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new home address, if validation succeeds
    def edit_home_address(self, user_to_edit: User, new_address: str):
        current_address = user_to_edit.home_address
        user_to_edit.home_address = new_address
        validation_result = address_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.home_address = current_address
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        user_to_edit.save()
        success_msg = user_to_edit.name + "\'s home address has been updated\n"
        return {'result': True, 'message': success_msg}

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new phone number, if validation succeeds
    def edit_phone(self, user_to_edit: User, new_phone: str):
        current_phone = user_to_edit.phone
        user_to_edit.phone = new_phone
        validation_result = phone_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.phone = current_phone
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        user_to_edit.save()
        success_msg = user_to_edit.name + "\'s phone number has been updated\n"
        return {'result': True, 'message': success_msg}

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new role, if validation succeeds
    def edit_role(self, user_to_edit: User, new_role: int):
        current_role = user_to_edit.role
        user_to_edit.role = new_role
        validation_result = role_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.role = current_role
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        user_to_edit.save()
        success_msg = user_to_edit.name + " now has the role of " + AccountType(user_to_edit.role).__str__() + "\n"
        return {'result': True, 'message': success_msg}

    # pre: Calling user is in the database
    # post: Returns a QueryList of all users that can be edited by calling user
    # side: None
    def list_of_editable_users(self) -> list[User]:
        list_of_users = [User.objects.get(user_id=self.user_id)]
        list_of_users += list(User.objects.all().exclude(user_id=self.user_id))
        return list_of_users

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: 1) Record in User table is updated with new skill, if validation succeeds
    #       2) skill is added to Skills table, if no other existing user has the skill
    def add_skill(self, user_to_edit: User, new_skill: str):
        trimmed_skill = new_skill.strip(" \n\t")
        if trimmed_skill == "":
            return {'result': False, 'message': "Can\'t add skill with no name\n"}

        lowercase_skill = trimmed_skill.lower()
        editing_self = self.user_id == user_to_edit.user_id
        if editing_self:
            skill_list_to_check = self.skills
            msg_to_return = "You already have the skill \"" + trimmed_skill + "\"\n"
        else:
            skill_list_to_check = set(User.objects.get(user_id=user_to_edit.user_id).skills.values_list(Lower('name'),
                                                                                                        flat=True))
            msg_to_return = user_to_edit.name + " already has the skill \"" + trimmed_skill + "\"\n"

        if lowercase_skill in skill_list_to_check:
            return {'result': False, 'message': msg_to_return}

        skill_to_add = Skill(name=trimmed_skill)
        if lowercase_skill in Skill.objects.values_list(Lower('name'), flat=True):
            skill_to_add.count = F('count') + 1
            success_msg = "Common skill \""
        else:
            success_msg = "Unique skill \""

        success_msg += trimmed_skill + "\" added to "
        if editing_self:
            success_msg += "your profile\n"
            self.skills.add(trimmed_skill)
        else:
            success_msg += user_to_edit.name + "\n"

        skill_to_add.save()
        user_to_edit.skills.add(skill_to_add)
        user_to_edit.save()

        return {'result': True, 'message': success_msg}

    # pre: Data in user_to_edit is of an existing user
    # post: Returns a dict object with the result and message about result
    # side: 1) Record in User table is updated with lost_skill removed, if user has the skill
    #       2) skill is removed from Skills table, if no other existing user has the skill
    def remove_skill(self, user_to_edit: User, lost_skill: str):
        trimmed_skill = lost_skill.strip(" \t\n")
        if trimmed_skill == "":
            return {'result': False, 'message': "Can\'t remove skill with no name\n"}

        lowercase_skill = trimmed_skill.lower()
        editing_self = self.user_id == user_to_edit.user_id
        if editing_self:
            skill_list_to_check = self.skills
            skill_list = list(skill_list_to_check)
            for x in range(len(skill_list)):
                skill_list[x] = skill_list[x].lower()
            skill_list_to_check = set(skill_list)
            msg_to_return = "You don\'t have the skill \"" + trimmed_skill + "\"\n"
        else:
            skill_list_to_check = set(User.objects.get(user_id=user_to_edit.user_id).skills.values_list(Lower('name'),
                                                                                                        flat=True))
            msg_to_return = user_to_edit.name + " doesn\'t have the skill \"" + trimmed_skill + "\"\n"

        if lowercase_skill not in skill_list_to_check:
            return {'result': False, 'message': msg_to_return}

        skill_to_decrement = Skill.objects.get(name=trimmed_skill)
        skill_to_decrement.count = F('count') - 1
        skill_to_decrement.save()
        skill_to_decrement.refresh_from_db()
        if skill_to_decrement.count == 0:
            Skill.objects.get(name=trimmed_skill).delete()
            success_msg = "unique skill \""
        else:
            skill_to_decrement.save()
            success_msg = "common skill \""

        success_msg = "You have removed the " + success_msg + trimmed_skill + "\" from "

        if editing_self:
            self.skills.remove(trimmed_skill)
            success_msg += "your profile\n"
        else:
            success_msg += user_to_edit.name + "\n"

        return {'result': True, 'message': success_msg}

    # pre: user_to_view is a User model object
    # post: Returns a dict object with a message and list of skills, if access to view is granted
    # side: None
    def list_skills(self, user_to_view: User):
        if self.user_id == user_to_view.user_id:
            return list(self.skills).sort()

        return list(User.objects.get(user_id=user_to_view.user_id).skills.values_list('name', flat=True)).sort()
