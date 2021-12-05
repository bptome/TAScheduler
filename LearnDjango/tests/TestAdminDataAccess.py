from django.test import TestCase

from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.models import Course, User


# precondition: none
# post condition: returns a UserAdmin for testing
def add_admin():
    test_admin = UserAdmin(1, "testAdmin", "tA1!", "testAdmin@test.com", "101 W. Wisconsin Ave, Milwaukee, WI 53203",
                           "(414)222-2571")
    return test_admin


# precondition: my_user is of User class type
# post condition: return user model type
# side effect: Save to database
def add_user_to_test_database(my_user):
    user_role = -1
    if my_user.role == "Admin":
        user_role = 1
    elif my_user.role == "Instructor":
        user_role = 2
    elif my_user.role == "TA":
        user_role = 3
    new_user = User()
    new_user.user_id = my_user.user_id
    new_user.name = my_user.name
    new_user.password = my_user.password
    new_user.email = my_user.email
    new_user.home_address = my_user.home_address
    new_user.phone = my_user.phone_number
    new_user.role = user_role
    new_user.save()
    return new_user


# precondition: my_user is of User class type
# post condition: return an array of String of the User fields we want to display
def get_user_info(my_user):
    user_role = ""
    if my_user.role == 1:
        user_role = "Admin"
    elif my_user.role == 2:
        user_role = "Instructor"
    else:
        user_role = "TA"
    return [my_user.name, my_user.password, my_user.email, my_user.home_address, user_role, my_user.phone]


# precondition: none
# post condition: returns an array of String for a test course's information
# side effect: saves a course to the database
def get_course1():
    test_course = Course(1, 361, "CS361", 0, [], "T 5:00-6:00", "Fall", "Undergrad", "fun")
    test_course.save()
    return ["CS361", "Jayson Rock", ["Lab 901"], "T 5:00-6:00", "Fall", "Undergrad", "fun"]


class TestDisplayCourses(TestCase):
    def setUp(self):
        self.testAdmin = add_admin()
        add_user_to_test_database(self.testAdmin)

    def test_zero_courses(self):
        failure_msg = "Empty courses did not return an empty array"
        self.assertEqual([], self.testAdmin.display_courses(), msg=failure_msg)

    def test_one_course(self):
        course1 = get_course1()
        failure_msg = "One course called CS361 should be returned"
        self.assertEqual([course1], self.testAdmin.display_courses(), msg=failure_msg)

    def test_two_courses(self):
        course1 = get_course1()
        test_course2 = Course(2, 351, "CS351", 0, [], "W 5:00-6:00", "Spring", "Undergrad", "hard")
        test_course2.save()
        course2 = ["CS351", "Henry Trimbach", ["Lab 900"], "W 5:00-6:00", "Spring", "Graduate", "hard"]
        failure_msg = "An array of 2 courses (CS361 and CS 351) should be returned"
        self.assertEqual([course1, course2], self.testAdmin.display_courses(), msg=failure_msg)

    def test_return_length(self):
        get_course1()
        failure_msg = "One course called CS361 should be returned"
        self.assertEqual(7, len(self.testAdmin.display_courses()), msg=failure_msg)

    def test_return_type(self):
        failure_msg = "Did not return the proper type"
        self.assertEqual(type(self.testAdmin.display_people()), type([""]), failure_msg)


# precondition: none
# post condition: returns a second UserAdmin for testing
def add_second_admin():
    secondAdmin = UserAdmin(2, "New Admin", "tA431!", "newAdmin@test.com",
                            "3308 N Downer Ave", "(414)225-2901")
    return add_user_to_test_database(secondAdmin)


# precondition: none
# post condition: returns an Instructor for testing
def add_instructor():
    instructor = Instructor(3, "Instr", "tA43sdf1!", "instructor@test.com",
                            "123 Sesame St.", "(414)664-2571")
    return add_user_to_test_database(instructor)


# precondition: none
# post condition: returns a TA for testing
def add_ta():
    ta = TA(4, "Some TA", "$ggsfdF!", "ta@test.com",
            "some place in Milwaukee", "(414)684-7645")
    return add_user_to_test_database(ta)


class TestDisplayPeople(TestCase):
    def setUp(self):
        self.testAdmin = add_admin()
        self.testAdminDB = add_user_to_test_database(self.testAdmin)
        self.adminInfo = get_user_info(self.testAdminDB)

    def test_zero_users(self):
        failure_msg = "No one new added did not return an array of the logged in user"
        self.assertEqual([self.adminInfo], self.testAdmin.display_people(), msg=failure_msg)

    def test_other_admin(self):
        new_admin = add_second_admin()
        testArray = [self.adminInfo, get_user_info(new_admin)]
        failure_msg = "One admin added did not return both admins"
        self.assertEqual(testArray, self.testAdmin.display_people(), msg=failure_msg)

    def test_instructor(self):
        new_instructor = add_instructor()
        testArray = [self.adminInfo, get_user_info(new_instructor)]
        failure_msg = "One instructor added did not return both admin and instructor"
        self.assertEqual(testArray, self.testAdmin.display_people(), msg=failure_msg)

    def test_TA(self):
        new_ta = add_ta()
        testArray = [self.adminInfo, get_user_info(new_ta)]
        failure_msg = "One TA added did not return both admin and TA"
        self.assertEqual(testArray, self.testAdmin.display_people(), msg=failure_msg)

    def test_three_different_user_types(self):
        new_admin = add_second_admin()
        new_instructor = add_instructor()
        new_ta = add_ta()
        testArray = [self.adminInfo, get_user_info(new_admin), get_user_info(new_instructor), get_user_info(new_ta)]
        failure_msg = "One of each type of user added did not return one of each type and TA"
        self.assertEqual(testArray, self.testAdmin.display_people(), msg=failure_msg)

    def test_invalid_role_id(self):
        ta = TA(5, "Some TA", "$ggsfdF!", "ta@test.com",
                "some place in Milwaukee", "(414)068-47645")
        add_user_to_test_database(ta)
        failure_msg = "Role ID is not 1-3"
        with self.assertRaises(Exception, msg=failure_msg):
            self.testAdmin.display_people()

    def test_return_type(self):
        failure_msg = "Did not return the proper type"
        self.assertEqual(type(self.testAdmin.display_people()), type([""]), failure_msg)


class TestDisplayPeopleField(TestCase):
    def setUp(self):
        self.testAdmin = add_admin()
        self.fields = ["name", "password", "email", "home address", "role", "phone"]

    def test_fields(self):
        failure_msg = "Did not return the proper fields for user information"
        self.assertEqual(self.fields, self.testAdmin.display_people_fields(), msg=failure_msg)

    def test_field_count(self):
        failure_msg = "Did not return the proper number of fields for user information"
        self.assertEqual(6, len(self.testAdmin.display_people_fields()), msg=failure_msg)

    def test_return_type(self):
        failure_msg = "Did not return the proper type"
        self.assertEqual(type(self.testAdmin.display_people_fields()), type([""]), failure_msg)
