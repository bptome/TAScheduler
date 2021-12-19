from abc import ABC, abstractmethod
from TAInformation.Models.account_type import AccountType
from TAInformation.models import Course, User, Lab, CourseTAJunction


class BaseUser(ABC):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        self.user_id = id_number
        self.name = name
        self.password = password
        self.email = email
        self.home_address = address
        self.phone_number = phone
        self.role = AccountType.DEFAULT

    # precondition: none
    # post condition: return an array of Course specific to the user
    @abstractmethod
    def display_courses(self):
        pass

    # precondition: none
    # post condition: return an array of User
    @abstractmethod
    def display_people(self):
        pass

    # precondition: none
    # post condition: return an array of User
    @abstractmethod
    def display_people_fields(self):
        pass

    # pre: new_admin is derived from type BaseUser
    # post: Returns a dict object with the result and message about result
    # side: Creates new user of specified role if all data is valid and user doesn't already exist
    def create_user(self, new_user):
        return {'result': False, 'message': "Only admins can create new users\n"}

    def create_lab(self, lab_name, description, course):
        return "You must be an Admin to add Labs"

    def assign_ta_to_lab(self, lab, user):
        return "You must be an Admin to add a TA to a Lab"

    def assign_ta_to_course(self, user, course):
        return "You must be an Admin to add TA to a course"

    def avaliableInstructors(self):
        arr = []
        for val in User.objects.filter(role=AccountType.INSTRUCTOR.value).values():
            arr.append(val["name"])
        return arr

    def avaliableTAs(self):
        arr = []
        for val in User.objects.filter(role=AccountType.TA.value).values():
            arr.append(val["name"])
        return arr

    def avaliableCourses(self):
        arr = []
        for val in Course.objects.all().values():
            arr.append(val["course_name"])
        return arr

    def avaliableLabs(self):
        arr = []
        for val in Lab.objects.all().values():
            arr.append(val["lab_name"])

        print(arr)
        return arr

    def taAssignments(self):
        assignments = []
        for val in CourseTAJunction.objects.all().values():

            arr = [val["user_id_id"], val["course_id_id"]]
            assignments.append(arr)
        # for val in User.objects.filter(role=AccountType.TA.value).values():
        #     # m = CourseTAJunction.objects.get(val["user_id"])
        #      if m.course_id:
        #         arr = [val["name"]] # val["course_id"]
        #         assignments.append(arr)


        return assignments
