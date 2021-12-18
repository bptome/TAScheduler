from TAInformation.Models.account_type import AccountType
from TAInformation.Models.base_user import BaseUser
from TAInformation.Models.validator_methods import *
from TAInformation.models import Course, User, LabCourseJunction, Lab


class TA(BaseUser):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        super().__init__(id_number, name, password, email, address, phone)
        self.role = AccountType.TA

    def display_courses(self):
        #TO DO: MUST BE CHANGED EVENTUALLY, JUST RETURNS ALL COURSES NOW
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
        print("here")
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
            print("here")
            user_content.append(user_information)
        return user_content

    def display_people_fields(self):
        return ["name", "email", "role", "phone"]

    # pre: None
    # post: Returns dict object with message of inability to create accounts
    def create_user(self, new_user):
        return {'result': False, 'message': "Only admins can create new users\n"}
