from django.test import TestCase

from TAInformation.Models.account_type import AccountType
from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.course import ClassCourse
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.models import Course, User, Lab, LabCourseJunction


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
    new_user = User()
    new_user.user_id = my_user.user_id
    new_user.name = my_user.name
    new_user.password = my_user.password
    new_user.email = my_user.email
    new_user.home_address = my_user.home_address
    new_user.phone = my_user.phone_number
    new_user.role = my_user.role.value
    new_user.save()
    return new_user


def get_course_zero_lab():
    User(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", 2, "(414)173-4567").save()
    Course(1, "CS337", 97, "W 5:00-6:00", "Spring", "Graduate", "hard").save()
    return ["CS337", "Bob Sorenson", "", "W 5:00-6:00", "Spring", "Graduate", "hard"]


def get_course_one_lab():
    User(99, "Jayson Rock", "jbusbf435", "jrock@uwm.edu", "Kenwood ave", 2, "(414)123-4567").save()
    Course(2, "CS361", 99, "T 5:00-6:00", "Fall", "Undergrad", "fun").save()
    Lab(1, "Lab 900", False, "boring lab").save()
    LabCourseJunction(1, 1, 2).save()
    return ["CS361", "Jayson Rock", " Lab 900", "T 5:00-6:00", "Fall", "Undergrad", "fun"]


def get_course_two_lab():
    User(98, "Henry Trimbach", "ter7ythg", "trimbach@uwm.edu", "Downer ave", 2, "(414)143-4867").save()
    Course(3, "CS351", 98, "W 900:00-6:00", "Fall", "Graduate", "EZ").save()
    Lab(1, "Lab 900", False, "boring lab").save()
    LabCourseJunction(2, 1, 3).save()
    Lab(2, "Lab 901", False, "not boring lab").save()
    LabCourseJunction(3, 2, 3).save()
    return ["CS351", "Henry Trimbach", " Lab 900 Lab 901", "W 900:00-6:00", "Fall", "Graduate", "EZ"]


class TestDisplayCourses(TestCase):
    def setUp(self):
        self.testAdmin = add_admin()
        add_user_to_test_database(self.testAdmin)

    def test_zero_courses(self):
        failure_msg = "Empty courses did not return an empty array"
        self.assertEqual([], self.testAdmin.display_courses(), msg=failure_msg)

    def test_one_course(self):
        course1 = get_course_one_lab()
        failure_msg = "One course called CS361 should be returned"
        self.assertEqual([course1], self.testAdmin.display_courses(), msg=failure_msg)

    def test_two_courses(self):
        course1 = get_course_one_lab()
        course2 = get_course_two_lab()
        failure_msg = "An array of 2 courses (CS361 and CS 351) should be returned"
        self.assertEqual([course1, course2], self.testAdmin.display_courses(), msg=failure_msg)

    def test_zero_lab(self):
        course1 = get_course_zero_lab()
        failure_msg = "One course called CS361 should be returned"
        self.assertEqual([course1], self.testAdmin.display_courses(), msg=failure_msg)

    def test_one_lab(self):
        course1 = get_course_one_lab()
        failure_msg = "One course called CS361 should be returned"
        self.assertEqual([course1], self.testAdmin.display_courses(), msg=failure_msg)

    def test_two_lab(self):
        course1 = get_course_two_lab()
        failure_msg = "One course called CS361 should be returned"
        self.assertEqual([course1], self.testAdmin.display_courses(), msg=failure_msg)

    def test_return_length(self):
        get_course_zero_lab()
        failure_msg = "One course called CS361 should be returned"
        self.assertEqual(1, len(self.testAdmin.display_courses()), msg=failure_msg)

    def test_return_field_length(self):
        get_course_zero_lab()
        failure_msg = "One course with 7 fields should be returned "
        self.assertEqual(7, len(self.testAdmin.display_courses()[0]), msg=failure_msg)

    def test_return_type(self):
        failure_msg = "Did not return the proper type"
        self.assertEqual(type(self.testAdmin.display_people()), type([""]), failure_msg)


# precondition: none
# post condition: returns a second UserAdmin for testing
def add_second_admin():
    secondAdmin = UserAdmin(2, "New Admin", "tA431!", "newAdmin@test.com",
                            "3308 N Downer Ave", "(414)225-2901")
    add_user_to_test_database(secondAdmin)
    return ["New Admin", "tA431!", "newAdmin@test.com",
            "3308 N Downer Ave", "Admin", "(414)225-2901"]


# precondition: none
# post condition: returns an Instructor for testing
def add_instructor():
    instructor = Instructor(3, "Instr", "tA43sdf1!", "instructor@test.com",
                            "123 Sesame St.", "(414)664-2571")
    add_user_to_test_database(instructor)
    return ["Instr", "tA43sdf1!", "instructor@test.com",
            "123 Sesame St.", "Instructor", "(414)664-2571"]


# precondition: none
# post condition: returns a TA for testing
def add_ta():
    ta = TA(4, "Some TA", "$ggsfdF!", "ta@test.com",
            "some place in Milwaukee", "(414)684-7645")
    add_user_to_test_database(ta)
    return ["Some TA", "$ggsfdF!", "ta@test.com",
            "some place in Milwaukee", "TA", "(414)684-7645"]


class TestDisplayPeople(TestCase):
    def setUp(self):
        self.testAdmin = add_admin()
        self.testAdminDB = add_user_to_test_database(self.testAdmin)
        self.adminInfo = ["testAdmin", "tA1!", "testAdmin@test.com", "101 W. Wisconsin Ave, Milwaukee, WI 53203",
                          "Admin",
                          "(414)222-2571"]

    def test_zero_users(self):
        failure_msg = "No one new added did not return an array of the logged in user"
        self.assertEqual([self.adminInfo], self.testAdmin.display_people(), msg=failure_msg)

    def test_other_admin(self):
        test_array = [self.adminInfo, add_second_admin()]
        failure_msg = "One admin added did not return both admins"
        self.assertEqual(test_array, self.testAdmin.display_people(), msg=failure_msg)

    def test_instructor(self):
        test_array = [self.adminInfo, add_instructor()]
        failure_msg = "One instructor added did not return both admin and instructor"
        self.assertEqual(test_array, self.testAdmin.display_people(), msg=failure_msg)

    def test_TA(self):
        test_array = [self.adminInfo, add_ta()]
        failure_msg = "One TA added did not return both admin and TA"
        self.assertEqual(test_array, self.testAdmin.display_people(), msg=failure_msg)

    def test_three_different_user_types(self):
        test_array = [self.adminInfo, add_second_admin(), add_instructor(), add_ta()]
        failure_msg = "One of each type of user added did not return one of each type and TA"
        self.assertEqual(test_array, self.testAdmin.display_people(), msg=failure_msg)

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
