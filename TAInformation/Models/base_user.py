from abc import ABC, abstractmethod
from TAInformation.Models.account_type import AccountType
from TAInformation.models import Course, User, Lab, CourseTAJunction, LabTAJunction, LabCourseJunction


class BaseUser(ABC):
    # Constructor
    def __init__(self, id_number: int, name: str, password: str, email: str, address: str, phone: str):
        self.user_id = id_number
        self.name = name
        self.password = password
        self.email = email
        self.home_address = address
        self.phone = phone
        self.role = AccountType.DEFAULT
        self.skills: set[str] = set(User.objects.filter(user_id=self.user_id).values_list('skills__name', flat=True))

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
    def edit_role(self, user_to_edit: User, new_role: int):
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

    # pre: user_to_view is a User model object
    # post: Returns a dict object with a message and list of skills, if access to view is granted
    # side: None
    def list_skills(self, user_to_view: User):
        pass

    # pre: Calling user is in the database
    # post: Returns a QueryList of all users that can be edited by calling user
    # side: None
    def list_of_editable_users(self) -> list[User]:
        pass

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



    def avaliableLabsandCourses(self):
        arr = []
        for val in LabCourseJunction.objects.all().values():
            if Lab.objects.filter(lab_id=val["lab_id_id"]).exists():
                temp = [Lab.objects.get(lab_id=val["lab_id_id"]).lab_name, Course.objects.get(course_id=val["course_id_id"]).course_name]
                arr.append(temp)

        return arr

    def taAssignments(self):
        assignments = []
        for val in CourseTAJunction.objects.all().values():

            arr = [val["user_id_id"], val["course_id_id"]]
            if LabTAJunction.objects.filter(user_id=val["user_id_id"]).exists():
                lab = LabTAJunction.objects.get(user_id=val["user_id_id"]).lab_id.lab_name
                print(lab)
                arr.append(lab)
            else:
                arr.append("Grader")
            assignments.append(arr)
        # for val in User.objects.filter(role=AccountType.TA.value).values():
        #     # m = CourseTAJunction.objects.get(val["user_id"])
        #      if m.course_id:
        #         arr = [val["name"]] # val["course_id"]
        #         assignments.append(arr)

        return assignments
