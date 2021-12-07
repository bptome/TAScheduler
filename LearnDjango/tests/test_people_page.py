from django.test import TestCase, Client

from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.instructor import Instructor
from TAInformation.models import Course
from tests.TestAdminDataAccess import add_user_to_test_database, add_second_admin, add_instructor, add_ta, \
    get_course_zero_lab, get_course_two_lab


class AdminAccess(TestCase):
    def setUp(self):
        self.user_a_info = ["Bryce Tome", "sfG76Fgh", "bptome@uwm.edu", "fake address 566", "Admin", "(414)546-3464"]
        self.user_a = UserAdmin(1, "Bryce Tome", "sfG76Fgh", "bptome@uwm.edu", "fake address 566", "(414)546-3464")
        add_user_to_test_database(self.user_a)
        self.client = Client()
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)

    def test_zero_courses(self):
        response = self.client.get("/courses/", {}, follow=True)
        failure_msg = "Empty courses did not return an empty array"
        self.assertEqual(response.context['courses'], [], msg=failure_msg)

    def test_one_course(self):
        course1 = get_course_zero_lab()
        response = self.client.get("/courses/", {}, follow=True)
        failure_msg = "One course should be visible"
        self.assertEqual(response.context['courses'], [course1], msg=failure_msg)

    def test_two_courses(self):
        course1 = get_course_zero_lab()
        course2 = get_course_two_lab()
        response = self.client.get("/courses/", {}, follow=True)
        failure_msg = "two courses should be visible"
        self.assertEqual(response.context['courses'], [course1, course2], msg=failure_msg)

    def test_two_lab_string_two_courses(self):
        course1 = get_course_two_lab()
        response = self.client.get("/courses/", {}, follow=True)
        failure_msg = "lab string for a course with two labs is incorrect"
        self.assertEqual(response.context['courses'][0][3], course1[3], msg=failure_msg)

    def test_return_length(self):
        get_course_zero_lab()
        response = self.client.get("/courses/", {}, follow=True)
        failure_msg = "One course called CS361 should be returned"
        self.assertEqual(len(response.context['courses']), 1, msg=failure_msg)

    def test_return_field_length(self):
        get_course_zero_lab()
        response = self.client.get("/courses/", {}, follow=True)
        failure_msg = "One course with 7 fields should be returned"
        self.assertEqual(len(response.context['courses'][0]), 7, msg=failure_msg)
