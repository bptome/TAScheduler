from django.test import TestCase, Client

from LearnDjango.tests.TestAdminDataAccess import add_user_to_test_database, add_second_admin, add_instructor, add_ta
from TAInformation.Models.admin import UserAdmin


class AdminAccess(TestCase):
    def setUp(self):
        self.user_a_info = ["Bryce Tome", "sfG76Fgh", "bptome@uwm.edu", "fake address 566", "Admin", "(414)546-3464"]
        self.user_a = UserAdmin(1, "Bryce Tome", "sfG76Fgh", "bptome@uwm.edu", "fake address 566", "(414)546-3464")
        add_user_to_test_database(self.user_a)
        self.client = Client()
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)

    def test_no_other_users(self):
        response = self.client.get("/people/", {}, follow=True)
        failure_msg = "Only logged in Admin should be visible"
        self.assertEqual(response.context['people'], [self.user_a_info], msg=failure_msg)

    def test_other_admin(self):
        test_array = [self.user_a_info, add_second_admin()]
        response = self.client.get("/people/", {}, follow=True)
        failure_msg = "Admin and other Admin should be visible"
        self.assertEqual(response.context['people'], test_array, msg=failure_msg)

    def test_instructor(self):
        test_array = [self.user_a_info, add_instructor()]
        response = self.client.get("/people/", {}, follow=True)
        failure_msg = "Admin and instructor should be visible"
        self.assertEqual(response.context['people'], test_array, msg=failure_msg)

    def test_TA(self):
        test_array = [self.user_a_info, add_ta()]
        response = self.client.get("/people/", {}, follow=True)
        failure_msg = "Admin and TA should be visible"
        self.assertEqual(response.context['people'], test_array, msg=failure_msg)

    def test_three_different_types(self):
        test_array = [self.user_a_info, add_second_admin(), add_instructor(), add_ta()]
        response = self.client.get("/people/", {}, follow=True)
        failure_msg = "Admin and other Admin should be visible"
        self.assertEqual(response.context['people'], test_array, msg=failure_msg)

    def test_labels(self):
        response = self.client.get("/people/", {}, follow=True)
        failure_msg = "All people text fields should be visible"
        self.assertEqual(response.context['labels'],
                         ["name", "password", "email", "home address", "role", "phone"], msg=failure_msg)

    def test_name(self):
        response = self.client.get("/people/", {}, follow=True)
        failure_msg = "Name should match Admin's name"
        self.assertEqual(response.context['name'], self.user_a.name, msg=failure_msg)
