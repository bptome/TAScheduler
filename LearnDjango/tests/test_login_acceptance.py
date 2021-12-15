from django.test import TestCase, Client
from django.http import request
from TAInformation.Models.account_type import AccountType
from TAInformation.models import User


class AccountLogInAcceptanceTestAdmin(TestCase):
    def setUp(self):
        user = User(email="admin@admin.com", password="admin", role=AccountType.ADMIN)
        user.save()
        self.client = Client()

    def test_successful_login(self):
        self.response = self.client.post("/login/", {"email": "admin@admin.com", "password": "admin"}, follow=True)

        self.assertEqual('/dashboard/', self.response.redirect_chain[0][0])
        self.assertEqual('admin@admin.com', self.response.context["email"], "email not passed from login to list")
        self.assertEqual(AccountType.ADMIN, self.response.context["role"], "logged in with wrong role")

    def test_unsuccessful_login_wrong_password(self):
        c = Client()
        r = c.post("login/", {"email": "admin@admin.com", "password": "hello"}, follow=True)
        self.assertEqual("wrong password", r.context["message"], "logged in with valid email and wrong password")
        self.assertEqual(AccountType.ADMIN, r.context["role"], "logged in with wrong role")

    def test_unsuccessful_login_wrong_email(self):
        c = Client()
        r = c.post("login/", {"email": "admin234@admin.com", "password": "admin"}, follow=True)
        self.assertEqual("no such account", r.context["message"],
                         "logged in with incorrect email that is not in database")
        self.assertEqual(AccountType.ADMIN, r.context["role"], "logged in with wrong role")

    def test_unsuccessful_login_invalid_email(self):
        c = Client()
        r = c.post("/login/", {"email": "admin.com", "password": "admin"}, follow=True)
        self.assertEqual("invalid input from email", r.context["message"], "logged in with invalid email")
        self.assertEqual(AccountType.ADMIN, r.context["role"], "logged in with wrong role")

    def test_unsuccessful_login_invalid_email_too_short(self):
        c = Client()
        r = c.post("/login/", {"email": "@admin.com", "password": "admin"}, follow=True)
        self.assertEqual("invalid input from email", r.context["message"], "logged in with invalid email- too short")
        self.assertEqual(AccountType.ADMIN, r.context["role"], "logged in with wrong role")

    def test_unsuccessful_login_empty_email_(self):
        c = Client()
        r = c.post("/login/", {"email": "", "password": "admin"}, follow=True)
        self.assertEqual("empty input field(s)", r.context["message"], "logged in with invalid email- empty")
        self.assertEqual(AccountType.ADMIN, r.context["role"], "logged in with wrong role")

    def test_unsuccessful_login_empty_email_and_password(self):
        c = Client()
        r = c.post("/login/", {"email": "", "password": ""}, follow=True)
        self.assertEqual("empty input field(s)", r.context["message"],
                         "logged in with invalid email and password- both empty")
        self.assertEqual(AccountType.ADMIN, r.context["role"], "logged in with wrong role")

    def test_unsuccessful_login_empty_password(self):
        c = Client()
        r = c.post("/login/", {"email": "admin@admin.com", "password": ""}, follow=True)
        self.assertEqual("wrong password", r.context["message"],
                         "logged in with valid email and wrong password- empty password")
        self.assertEqual(AccountType.ADMIN, r.context["role"], "logged in with wrong role")


class AccountLogInAcceptanceTestInstructor(TestCase):
    def setUp(self):
        user = User(email="admin@admin.com", password="admin", role=AccountType.INSTRUCTOR)
        user.save()
        self.client = Client()

    def test_successful_login(self):
        self.response = self.client.post("/login/", {"email": "instructor@instructor.com", "password": "instructor"},
                                         follow=True)

        self.assertEqual('/dashboard/', self.response.redirect_chain[0][0])
        self.assertEqual('instructor@instructor.com', self.response.context["email"],
                         "email not passed from login to list")
        self.assertEqual(AccountType.INSTRUCTOR, self.response.context["role"], "logged in with wrong role")

    def test_unsuccessful_login_wrong_password(self):
        c = Client()
        r = c.post("login/", {"email": "instructor@instructor.com.com", "password": "hello"}, follow=True)
        self.assertEqual("wrong password", r.context["message"], "logged in with valid email and wrong password")
        self.assertEqual(AccountType.ADMIN, r.context["role"], "logged in with wrong role")


class AccountLogInAcceptanceTestTA(TestCase):
    def setUp(self):
        user = User(email="TA@TA.com", password="TA", role=AccountType.TA)
        user.save()
        self.client = Client()

    def test_successful_login(self):
        self.response = self.client.post("/login/", {"email": "TA@TA.com", "password": "TA"}, follow=True)

        self.assertEqual('/dashboard/', self.response.redirect_chain[0][0])
        self.assertEqual('TA@TA.com', self.response.context["email"], "email not passed from login to list")
        self.assertEqual(AccountType.TA, self.response.context["role"], "logged in with wrong role")

    def test_unsuccessful_login_wrong_password(self):
        c = Client()
        r = c.post("login/", {"email": "TA@TA.com.com", "password": "hello"}, follow=True)
        self.assertEqual("wrong password", r.context["message"], "logged in with valid email and wrong password")
        self.assertEqual(AccountType.ADMIN, r.context["role"], "logged in with wrong role")
