from django.test import TestCase
from django.test import Client
from TAInformation.models import Course, User


# Functions to setup all tests
class test_editAdminUserEmail(TestCase):
    def setUp(self):
        user = User(
            name="rock", password="1234", email="rock@email.com", home_address="2255 N . Lake Dr"
            , phone="(414)111-1111"

        )
        user.save()
        self.client = Client()

    def test_EditPhoneNUmber(self):
        # Act
        self.client.post("/", {"name": "rock", "password": "1234", "email": "email@email.com",
                               "home_address": "2255 N . Lake Dr", "phone": "(414)111-1112"})
        # assert
        self.assertEqual("(414)111-1112", r.context["Phone"], msg='user Edit his phone number successfully')

    def test_editAddress(self):
        # Act
        self.client.post("/", {"name": "rock", "password": "1234", "email": "email@email.com",
                               "home_address": "2255 N . wisconsin ST", "phone": "(414)111-1112"})
        # assert
        self.assertEqual("2255 N . wisconsin ST", r.context["home_address"], msg='user Edit his address successfully')

    def test_editEmail(self):
        # Act
        self.client.post("/", {"name": "rock", "password": "1234", "email": "Email@email.com",
                               "home_address": "2255 N . wisconsin ST", "phone": "(414)111-1112"})
        # assert
        self.assertEqual("Email@email.com", r.context["email"], msg='user Edit his email successfully')

    def test_editInformation(self):
        # Act
        self.client.post("/", {"name": "Z", "password": "12345", "email": "Z@email.com",
                               "home_address": "2255 N . wisconsin ST", "phone": "(414)111-1112"})
        # assert
        self.assertEqual("Z@email.com", r.context["email"], msg='user Edit his information successfully')
