from TAInformation.Models.base_user import BaseUser
from TAInformation.Models.account_type import AccountType
from TAInformation.Models.validator_methods import *
from TAInformation.models import Course, User, LabCourseJunction, Lab, LabTAJunction, CourseTAJunction


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

    # pre: lab_name is a String, has_grader is a boolean, description is a String, course_id is the pk for Course
    # post: success message
    # side: saves a new lab to the DB, saves a new lab to course junction to the DB
    def create_lab(self, lab_name, has_grader, description, course):
        if Lab.objects.filter(lab_name=lab_name).exists():
            for junction in LabCourseJunction.objects.filter(course_id=course):
                if LabCourseJunction.objects.filter(lab_id=junction.lab_id, course_id=course):
                    return "Lab name already created for this course"
        lab = Lab.objects.create(lab_name=lab_name, has_grader=has_grader, description=description)
        LabCourseJunction.objects.create(lab_id=lab, course_id=course)
        return "Lab saved to course"

    # pre: lab_id is a Lab primary key, user_id is a User primary key
    # post: success message
    # side: saves a new assignment junction for a lab and a TA
    def assign_ta_to_lab(self, user, lab):
        global course
        if user.role != AccountType.TA.value:
            return "Only TA can be added to lab"
        if LabTAJunction.objects.filter(lab_id=lab, user_id=user).exists():
            return "TA already in lab"
        LabTAJunction.objects.create(lab_id=lab, user_id=user)
        for junction in LabCourseJunction.objects.filter(lab_id=lab):
            course = junction.course_id
        for junction in CourseTAJunction.objects.filter(user_id=user):
            if junction.course_id == course:
                return "TA assigned to lab"
        CourseTAJunction.objects.create(user_id=user, course_id=course)
        return "TA assigned to lab and course"


    # pre: course_id is a Course primary key, user_id is a User primary key
    # post: Return an error message
    def assign_ta_to_course(self, user, course):
        if user.role != AccountType.TA.value:
            return "Only TA can be added to a course"
        if CourseTAJunction.objects.filter(user_id=user, course_id=course).exists():
            return "TA already in this course"
        CourseTAJunction.objects.create(user_id=user, course_id=course)
        return "TA assigned to course"

