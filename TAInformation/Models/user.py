from abc import ABC, abstractmethod


class User(ABC):

    # precondition: id: Int, name: String, email: String, home_address: String, role: String, phone: String
    # post condition: creates a user and sets fields
    def __init__(self, id, name, password, email, home_address, role, phone):
        self.id = id
        self.name = name
        self.password = password
        self.email = email
        self.home_address = home_address
        self.role = role
        self.phone = phone

    # precondition: none
    # post condition: return an array of Course specific to the user
    def display_courses(self):
        return

    # precondition: none
    # post condition: return an array of User
    @abstractmethod
    def display_people(self):
        pass

    @abstractmethod
    def display_people_fields(self):
        pass
