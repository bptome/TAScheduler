from TAInformation.Models.base_user import BaseUser
from TAInformation.Models.account_type import AccountType
from TAInformation.models import Course, User


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
            course_information = [
                course.course_name,
                User.objects.get(user_id=course.instructor_id).name,
                course.lab,
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
                str(my_user.phone)
            ]
            user_content.append(user_information)
        return user_content

    def display_people_fields(self):
        return ["name", "password", "email", "home address", "role", "phone"]

    def create_admin(self, new_admin: BaseUser):
        if new_admin.role != AccountType.ADMIN:
            return False

    def __create_user_validator(self, new_admin: BaseUser):
        pass
