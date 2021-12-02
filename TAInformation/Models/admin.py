from TAInformation.Models import user
from TAInformation.models import User, Course


class UserAdmin(user.User):

    # precondition: none
    # post condition: returns a  return n array of [String] for all course's name, instructor name, lab names as [String], semester,
    def display_courses(self):
        return

    # precondition: none
    # post condition: return n array of [String] for all people's name, password, email,
    # home_address, role and phone number and a String array of all people and their public and private info
    # side effect: raises an exception if role is not valid number
    def display_people(self):
        return

    # precondition: none
    # post condition: return an array of String for the field description name, password, email,
    # home address, role, phone
    def display_people_fields(self):
        return ["name", "password", "email", "home address", "role", "phone"]
