from django.test import TestCase
from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.Models.validator_methods import *
from TAInformation.Models.account_type import AccountType


class EditAccountsAsAdminWithValidData(TestCase):
    def setUp(self):
        self.testAdmin = UserAdmin(-1, "", "", "", "", "")
        self.editTA = User(user_id=2, name="Name to be edited later", email="namedlater@test.com", password="p2BNl$",
                           home_address="Address to be edited later", phone="(414)555-9999", role=AccountType.TA.value)
        all_tests_setup(self.testAdmin, 1, "testAdmin", "tA1)", "testAdmin@test.com",
                        "101 E. Wisconsin Ave., Milwaukee, WI 53202", "(414)555-0001")
        self.editTA.save()

    def test_edit_id_to_unused(self):
        result_info = self.testAdmin.edit_user_id(self.editTA, 11)
        self.assertTrue(result_info['result'], msg="User ID wasn\'t changed to 11, despite no user "
                                                                      "having that ID number")

    def test_edit_id_to_used(self):
        result_info = self.testAdmin.edit_user_id(self.editTA, self.testAdmin.user_id)
        self.assertEqual(result_info['message'],
                         "User with given ID already exists",
                         msg="Admin was able to change ID number to one already taken by another user")

    def test_edit_name_valid_length(self):
        result_info = self.testAdmin.edit_name(self.editTA, "editTA")
        self.assertTrue(result_info['result'], msg="Admin wasn\'t able to change the user\'s name")

    def test_edit_email_to_unused(self):
        result_info = self.testAdmin.edit_email(self.editTA, "editTA@test.com")
        self.assertTrue(result_info['result'],
                        msg="Admin wasn\'t able to change email despite no other user having the given email address")

    def test_edit_email_to_used(self):
        result_info = self.testAdmin.edit_email(self.editTA, self.testAdmin.email)
        self.assertEqual(result_info['message'], "User with given email already exists",
                         msg="Admin was able to edit user email to one already used by another user")

    def test_edit_password(self):
        result_info = self.testAdmin.edit_password(self.editTA, "gTg1*")
        self.assertTrue(result_info['result'], msg="Admin wasn\'t able to change password to valid password")

    def test_edit_home_address(self):
        result_info = self.testAdmin.edit_home_address(self.selfTA, self.testAdmin.home_address)
        self.assertTrue(result_info['result'], msg="Admin wasn\'t able to change user\'s home address to valid address")

    def test_edit_phone_number(self):
        result_info = self.testAdmin.edit_phone_number(self.editTA, self.testAdmin.phone_number)
        self.assertTrue(result_info['result'], msg="Admin wasn\'t able to change user\'s phone number to valid number")

    def tearDown(self):
        User.objects.all().delete()


class EditAccountsAsAdminWithInvalidData(TestCase):
    def setUp(self):
        self.testAdmin = UserAdmin(-1, "", "", "", "", "")
        self.editTA = User(user_id=2, name="Name to be edited later", email="namedlater@test.com", password="p2BNl$",
                           home_address="Address to be edited later", phone="(414)555-9999", role=AccountType.TA.value)
        all_tests_setup(self.testAdmin, 1, "testAdmin", "tA1)", "testAdmin@test.com",
                        "101 E. Wisconsin Ave., Milwaukee, WI 53202", "(414)555-0001")
        self.editTA.save()

    #def test_edit_name_too_short(self):
       # result_info = self.testAdmin.edit_name(self.editTA, "edit")
       # self.assertEqual(result_info['message'], "Given name was too short",
                       #  msg="Admin was able to edit user\'s name to one that\'s <= 5 characters")

    def tearDown(self):
        User.objects.all().delete()

class EditAccountsAsInstructorWithValidData(TestCase):


class EditAccountsAsInstructorWithInvalidData(TestCase):


class EditAccountsAsTAWithValidData(TestCase):


class EditAccountsAsTAWithInvalidData(TestCase):


class DropDownListPopulation(TestCase):