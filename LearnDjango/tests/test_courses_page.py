from django.test import TestCase, Client

from TAInformation.Models.admin import UserAdmin
from tests.TestAdminDataAccess import add_user_to_test_database, add_second_admin, add_instructor, add_ta


class AdminAccess(TestCase):
    def setUp(self):
        self.user_a_info = ["Bryce Tome", "sfG76Fgh", "bptome@uwm.edu", "fake address 566", "Admin", "(414)546-3464"]
        self.user_a = UserAdmin(1, "Bryce Tome", "sfG76Fgh", "bptome@uwm.edu", "fake address 566", "(414)546-3464")
        add_user_to_test_database(self.user_a)
        self.client = Client()

    def test_no_other_users(self):
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "Only logged in Admin should be visible"
        self.assertEqual(self.firstResponse.context['people'], [self.user_a_info], msg=failure_msg)

    def test_other_admin(self):
        test_array = [self.user_a_info, add_second_admin()]
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "Admin and other Admin should be visible"
        self.assertEqual(self.firstResponse.context['people'], test_array, msg=failure_msg)

    def test_instructor(self):
        test_array = [self.user_a_info, add_instructor()]
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "Admin and instructor should be visible"
        self.assertEqual(self.firstResponse.context['people'], test_array, msg=failure_msg)

    def test_TA(self):
        test_array = [self.user_a_info, add_ta()]
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "Admin and TA should be visible"
        self.assertEqual(self.firstResponse.context['people'], test_array, msg=failure_msg)

    def test_three_different_types(self):
        test_array = [self.user_a_info, add_second_admin(), add_instructor(), add_ta()]
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "Admin and other Admin should be visible"
        self.assertEqual(self.firstResponse.context['people'], test_array, msg=failure_msg)

    def test_labels(self):
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "All people text fields should be visible"
        self.assertEqual(self.firstResponse.context['labels'],
                         ["name", "password", "email", "home address", "role", "phone"], msg=failure_msg)

    def test_name(self):
        self.firstResponse = self.client.post("/", {"name": "admin", "password": "password123"}, follow=True)
        failure_msg = "Name should match Admin's name"
        self.assertEqual(self.firstResponse.context['name'], self.user_a.name, msg=failure_msg)
