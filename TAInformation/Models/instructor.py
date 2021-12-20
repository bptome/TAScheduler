from django.db.models import F
from django.db.models.functions import Lower

from TAInformation.Models.account_type import AccountType
from TAInformation.Models.base_user import BaseUser

from TAInformation.Models.validator_methods import email_validator, password_validator, address_validator, phone_validator
from TAInformation.models import Course, User, LabCourseJunction, Lab, Skill


class Instructor(BaseUser):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        super().__init__(id_number, name, password, email, address, phone)
        self.role = AccountType.INSTRUCTOR
    # precondition: none
    # post condition: return an array of all Course assignments for instructor
    def display_courses(self):
        all_courses = Course.objects.filter(instructor_id=self.user_id)
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
                my_user.email,
                AccountType(my_user.role).__str__(),
                my_user.phone
            ]
            user_content.append(user_information)
        return user_content

    def display_people_fields(self):
        return ["name", "email", "role", "phone"]

    # pre: None
    # post: Returns dict object with message of inability to create accounts
    def create_user(self, new_user):
        return {'result': False, 'message': "Only admins can create new users\n"}

    # pre: None
    # post: Returns a dict object with the result and message about inability to edit their user id
    # side: None
    def edit_user_id(self, user_to_edit: User, new_user_id: int):
        return {'result': False, 'message': "Only admins can change user ids\n"}

    # pre: None
    # post: Returns a dict object with the result and message about inability to edit their name
    # side: None
    def edit_name(self, user_to_edit: User, new_name: str):
        return {'result': False, 'message': "Only admins can change names\n"}

    # pre: user_to_edit has data of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new email, if validation succeeds and email doesn't belong to another
    #       user
    def edit_email(self, user_to_edit: User, new_email: str):
        if user_to_edit.user_id != self.user_id:
            return {'result': False, 'message': "Instructors can only edit their own email address\n"}

        current_email = user_to_edit.email
        user_to_edit.email = new_email
        validation_result = email_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.email = current_email
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        if User.objects.filter(email=user_to_edit.email).exists():
            user_to_edit.email = current_email
            return {'result': False, 'message': "An user in the system already has that email\n"}

        user_to_edit.save()
        return {'result': True, 'message': "Your email address has been successfully changed\n"}

    # pre: user_to_edit has data of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new password, if validation succeeds
    def edit_password(self, user_to_edit: User, new_password: str):
        if user_to_edit.user_id != self.user_id:
            return {'result': False, 'message': "Instructors can only edit their own password\n"}

        current_password = user_to_edit.password
        user_to_edit.password = new_password
        validation_result = password_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.password = current_password
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        user_to_edit.save()
        return {'result': True, 'message': "Your password has been successfully changed\n"}

    # pre: user_to_edit has data of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new home address, if validation succeeds
    def edit_home_address(self, user_to_edit: User, new_address: str):
        if user_to_edit.user_id != self.user_id:
            return {'result': False, 'message': "Instructors can only edit their own home address\n"}

        current_address = user_to_edit.home_address
        user_to_edit.home_address = new_address
        validation_result = address_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.home_address = current_address
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        user_to_edit.save()
        return {'result': True, 'message': "Your home address has been successfully updated\n"}

    # pre: user_to_edit has data of an existing user
    # post: Returns a dict object with the result and message about result
    # side: Record in User table is updated with new phone number, if validation succeeds
    def edit_phone(self, user_to_edit: User, new_phone: str):
        if user_to_edit.user_id != self.user_id:
            return {'result': False, 'message': "Instructors can only edit their own phone number\n"}

        current_phone = user_to_edit.phone
        user_to_edit.phone = new_phone
        validation_result = phone_validator(user_to_edit)

        if not validation_result['result']:
            user_to_edit.phone = current_phone
            return {'result': validation_result['result'], 'message': validation_result['errorMsg']}

        user_to_edit.save()
        return {'result': True, 'message': "Your phone number has been successfully updated"}

    # pre: None
    # post: Returns a dict object with the result and message about inability to edit role
    # side: None
    def edit_role(self, user_to_edit: User, new_role: int):
        return {'result': False, 'message': "Instructors can\'t change anyone\'s role\n"}

    # pre: Calling user is in the database
    # post: Returns a QueryList of all users that can be edited by calling user
    # side: None
    def list_of_editable_users(self) -> list[User]:
        return list(User.objects.filter(user_id=self.user_id))

    # pre: user_to_edit has data of an existing user
    # post: Returns a dict object with the result and message about result
    # side: 1) Record in User table is updated with new skill, if validation succeeds
    #       2) skill is added to Skills table, if no other existing user has the skill
    def add_skill(self, user_to_edit: User, new_skill: str):
        if user_to_edit.user_id != self.user_id:
            error_msg = "You can\'t add skills to " + user_to_edit.name + "\n"
            return {'result': False, 'message': error_msg}

        trimmed_skill = new_skill.strip(" \n\t")
        if trimmed_skill == "":
            return {'result': False, 'message': "Can\'t add skill with no name\n"}

        lowercase_skill = trimmed_skill.lower()
        skills_list = list(self.skills)
        for x in range(len(skills_list)):
            skills_list[x] = skills_list[x].lower()

        if lowercase_skill in skills_list:
            msg_to_return = "You already have the skill \"" + trimmed_skill + "\"\n"
            return {'result': False, 'message': msg_to_return}

        skill_to_add = Skill(name=trimmed_skill)
        if lowercase_skill in Skill.objects.values_list(Lower('name'), flat=True):
            skill_to_add.count = F('count') + 1
            success_msg = "Common skill \""
        else:
            success_msg = "Unique skill \""

        success_msg += trimmed_skill + "\" added to your profile\n"
        skill_to_add.save()
        user_to_edit.skills.add(skill_to_add)
        user_to_edit.save()
        self.skills.add(trimmed_skill)
        return {'result': True, 'message': success_msg}

    # pre: user_to_edit has data of an existing user
    # post: Returns a dict object with the result and message about result
    # side: 1) Record in User table is updated with lost_skill removed, if user has the skill
    #       2) skill is removed from Skills table, if no other existing user has the skill
    def remove_skill(self, user_to_edit: User, lost_skill: str):
        if user_to_edit.user_id != self.user_id:
            error_msg = "You can\'t remove skills from " + user_to_edit.name + "\n"
            return {'result': False, 'message': error_msg}

        trimmed_skill = lost_skill.strip(" \t\n")
        if trimmed_skill == "":
            return {'result': False, 'message': "Can\'t remove skill with no name\n"}

        lowercase_skill = trimmed_skill.lower()
        skills_list = list(self.skills)
        for x in range(len(skills_list)):
            skills_list[x] = skills_list[x].lower()

        if lowercase_skill not in skills_list:
            error_msg = "You don\'t have the skill \"" + trimmed_skill + "\"\n"
            return {'result': False, 'message': error_msg}

        self.skills.remove(trimmed_skill)
        skill_to_decrement = Skill.objects.get(name=trimmed_skill)
        user_to_edit.skills.remove(skill_to_decrement)
        skill_to_decrement.count = F('count') - 1
        skill_to_decrement.save()
        skill_to_decrement.refresh_from_db()

        if skill_to_decrement.count == 0:
            Skill.objects.get(name=trimmed_skill).delete()
            success_msg = "unique skill \""
        else:
            skill_to_decrement.save()
            success_msg = "common skill \""

        success_msg = "You have removed the " + success_msg + trimmed_skill + "\" from your profile\n"
        return {'result': True, 'message': success_msg}

    # pre: user_to_view is a User model object
    # post: Returns a dict object with a message and list of skills, if access to view is granted
    # side: None
    def list_skills(self, user_to_view: User):
        if user_to_view.user_id != self.user_id:
            return {'result': False, 'message': "You can only view your skills\n"}

        return list(self.skills).sort()
