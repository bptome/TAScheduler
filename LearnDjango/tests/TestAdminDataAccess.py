from django.test import TestCase, Client

from TAInformation.models import Course, UserAdmin


def add_admin():
    test_admin = UserAdmin(1, "testAdmin", "tA1!", "testAdmin@test.com", "101 W. Wisconsin Ave, Milwaukee, WI 53203",
                       "(414)222-2571")
    return test_admin


class TestDisplayCourses(TestCase):
    def setUp(self):
        self.testAdmin = add_admin()

    def test_zero_courses(self):
        failure_msg = "Empty courses did not return an empty array"
        self.assertEqual([], self.testAdmin.display_courses(), msg=failure_msg)

    def test_one_course(self):
        testCourse = Course(1, 361, "CS361", 0, [], "T 5:00-6:00", "Fall", "Undergrad", "fun")
        testCourse.save()
        failure_msg = "One course called CS361 should be returned"
        self.assertEqual([testCourse], self.testAdmin.display_courses(), msg=failure_msg)

    def test_two_courses(self):
        testCourse = Course(1, 361, "CS361", 0, [], "T 5:00-6:00", "Fall", "Undergrad", "fun")
        testCourse.save()
        testCourse2 = Course(2, 351, "CS351", 0, [], "W 5:00-6:00", "Spring", "Undergrad", "hard")
        testCourse2.save()
        failure_msg = "An array of 2 courses (CS361 and CS 351) should be returned"
        self.assertEqual([testCourse, testCourse2], self.testAdmin.display_courses(), msg=failure_msg)

class TestDisplayUsers(TestCase):
    def setup(self):
        self.testAdmin = add_admin()

    # def test_zero_users(self):

    # def test_one_user(self):
    #
    # def test_two_user(self):
    #
    # def test_other_admin(self):
    #
    # def test_instructor(self):
    #
    # def test_TA(self):
    #
    # def test_three_different_user_types(self):
    #
    # def test_public_info(self, user):
    #
    # def test_private_info(self, user):