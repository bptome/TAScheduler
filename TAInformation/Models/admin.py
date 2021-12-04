
from TAInformation.Models.base_user import BaseUser
from TAInformation.models import Course, User
from TAInformation.Models.account_type import AccountType


class UserAdmin(BaseUser):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        super().__init__(id_number, name, password, email, address, phone)
        self.role = AccountType.ADMIN

    # precondition: none
    # post condition: return an array of all Courses
    def display_courses(self):
        all_courses = Course.objects.all()
        course_content = []
        for course in all_courses:
            course_content.append(course.course_name)
        return course_content

    # precondition: none
    # post condition: return a String array of all people and their public and private info
    def display_people(self):
        # testing how this works
        all_users = User.objects.all()
        user_content = []
        for user in all_users:
            user_content.append(user.name)
        return user_content

    def create_admin(self, new_admin: BaseUser):
        if new_admin.role != AccountType.ADMIN:
            return False

    def __create_user_validator(self, new_admin: BaseUser):
        pass





