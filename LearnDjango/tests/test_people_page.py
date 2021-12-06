from django.test import TestCase, Client

from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.instructor import Instructor
from TAInformation.models import Course
from tests.TestAdminDataAccess import add_user_to_test_database, add_second_admin, add_instructor, add_ta, get_course1


class AdminAccess(TestCase):
    def setUp(self):
        self.user_a_info = ["Bryce Tome", "sfG76Fgh", "bptome@uwm.edu", "fake address 566", "Admin", "(414)546-3464"]
        self.user_a = UserAdmin(1, "Bryce Tome", "sfG76Fgh", "bptome@uwm.edu", "fake address 566", "(414)546-3464")
        add_user_to_test_database(self.user_a)
        self.client = Client()

    def test_zero_courses(self):
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "Empty courses did not return an empty array"
        self.assertEqual(self.firstResponse.context['courses'], [], msg=failure_msg)

    def test_one_course(self):
        course1 = get_course1()
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "One course should be visible"
        self.assertEqual(self.firstResponse.context['courses'], [course1], msg=failure_msg)

    def test_two_courses(self):
        course1 = get_course1()
        henry_trimbach = Instructor(98, "Henry Trimbach", "ter7ythg", "trimbach@uwm.edu", "Downer ave", "(414)143-4867")
        add_user_to_test_database(henry_trimbach).save()
        test_course2 = Course(2, 351, "CS351", 98, "Lab 900", "W 5:00-6:00", "Spring", "Graduate", "hard")
        test_course2.save()
        course2 = ["CS351", "Henry Trimbach", "Lab 900", "W 5:00-6:00", "Spring", "Graduate", "hard"]
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "two courses should be visible"
        self.assertEqual(self.firstResponse.context['courses'], [course1, course2], msg=failure_msg)

    def test_return_length(self):
        get_course1()
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "One course called CS361 should be returned"
        self.assertEqual(len(self.firstResponse.context['courses']), 1, msg=failure_msg)

    def test_return_field_length(self):
        get_course1()
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "One course with 7 fields should be returned"
        self.assertEqual(len(self.firstResponse.context['courses'][0]), 7, msg=failure_msg)
