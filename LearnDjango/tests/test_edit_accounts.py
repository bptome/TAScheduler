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
        result_info = self.testAdmin.edit_phone(self.editTA, self.testAdmin.phone)
        self.assertTrue(result_info['result'], msg="Admin wasn\'t able to change user\'s phone number to valid number")

    def test_edit_role(self):
        result_info = self.testAdmin.edit_role(self.editTA, AccountType.INSTRUCTOR)
        self.assertTrue(result_info['result'], msg="Admin wasn\'t able to changed user\'s role to Instructor")

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

    def test_edit_user_id_neg(self):
        result_info = self.testAdmin.edit_user_id(self.editTA, -1)
        self.assertEqual(result_info['message'], "Invalid user id entered\n",
                         msg="Admin was able to edit user ID to negative number")

    def test_edit_user_id_blank(self):
        result_info = self.testAdmin.edit_user_id(self.editTA, "")
        self.assertEqual(result_info['message'], "Invalid user id entered\n",
                         msg="Admin was able to edit user ID to an empty string")

    def test_edit_name_too_short(self):
       result_info = self.testAdmin.edit_name(self.editTA, "edit")
       self.assertEqual(result_info['message'], "Given name was too short",
                        msg="Admin was able to edit user\'s name to one that\'s <= 5 characters")

    def test_edit_email(self):
        result_info = self.testAdmin.edit_email(self.editTA, "test.com")
        self.assertFalse(result_info['result'], msg="Admin was able to edit user ID to negative number")

    def test_edit_password_too_short(self):
        result_info = self.testAdmin.edit_password(self.editTA, "pT&")
        self.assertEqual(result_info['message'], "Password must be at least 4 characters long\n",
                         msg="Admin was able to change password to one shorter than the minimum length needed")

    def test_edit_password_missing_number(self):
        result_info = self.testAdmin.edit_password(self.editTA, "pT&!")
        self.assertEqual(result_info['message'], "Password must contain >= 1 number\n",
                         msg="Admin was able to change password to one missing a number")

    def test_edit_password_missing_uppercase(self):
        result_info = self.testAdmin.edit_password(self.editTA, "pt&1")
        self.assertEqual(result_info['message'], "Password must contain >= 1 uppercase letter\n",
                         msg="Admin was able to change password to one missing an uppercase letter")

    def test_edit_password_missing_lowercase(self):
        result_info = self.testAdmin.edit_password(self.editTA, "PT&1")
        self.assertEqual(result_info['message'], "Password must contain >= 1 lowercase letter\n",
                         msg="Admin was able to change password to one missing an lowercase letter")

    def test_edit_password_missing_special(self):
        result_info = self.testAdmin.edit_password(self.editTA, "ptB1")
        self.assertEqual(result_info['message'], "Password must contain >= 1 non-alphanumeric character\n",
                         msg="Admin was able to change password to one missing a non-alphanumeric character")

    def test_edit_home_address_blank(self):
        result_info = self.testAdmin.edit_home_address(self.editTA, "")
        self.assertEqual(result_info['message'], "Home address is missing\n",
                         msg="Admin was able to change user\'s home address to an empty string")

    def test_edit_home_address_spaces(self):
        result_info = self.testAdmin.edit_home_address(self.editTA, "  ")
        self.assertEqual(result_info['message'], "Home address must contain some non-space characters\n",
                         msg="Admin was able to change user\'s home address to a string with only spaces in it")

    def test_edit_phone_blank(self):
        result_info = self.testAdmin.edit_phone(self.editTA, "")
        self.assertEqual(result_info['message'], "No phone number given\n",
                         msg="Admin was able to change user\'s phone number to an empty string")

    def test_edit_phone_wrong_amount(self):
        result_info = self.testAdmin.edit_phone(self.editTA, "4145550123")
        self.assertEqual(result_info['message'], "Phone number should have exactly 13 characters\n",
                         msg="Admin was able to change user\'s phone number to an string that doesn\'t have exactly 13 characters")

    def test_edit_phone_misplaced(self):
        result_info = self.testAdmin.edit_phone(self.editTA, "(414)A55-0123")
        self.assertEqual(result_info['message'], "Misplaced character in phone number entry\n",
                         msg="Admin was able to change user\'s phone number to one that has a non-digit in a place that one is expected")

    def test_edit_phone_lead_parentheses(self):
        result_info = self.testAdmin.edit_phone(self.editTA, "1414)555-0123")
        self.assertEqual(result_info['message'], "Missing lead parentheses in phone number entry\n",
                         msg="Admin was able to change user\'s phone number to one that doesn\'t have a lead parentheses")

    def test_edit_phone_trail_parentheses(self):
        result_info = self.testAdmin.edit_phone(self.editTA, "(4141555-0123")
        self.assertEqual(result_info['message'], "Missing trailing parentheses in phone number entry\n",
                         msg="Admin was able to change user\'s phone number to one that doesn\'t have a trailing parentheses in its expected place")

    def test_edit_phone_dash(self):
        result_info = self.testAdmin.edit_phone(self.editTA, "(414)55510123")
        self.assertEqual(result_info['message'], "Missing dash between prefix and suffix in phone number entry\n",
                         msg="Admin was able to change user\'s phone number to one that doesn\'t have a dash in its expected place")

    def test_edit_role_default(self):
        result_info = self.testAdmin.edit_role(self.editTA, AccountType.DEFAULT)
        self.assertEqual(result_info['message'], "User can\'t be changed to default role\n",
                         msg="Admin was somehow able to change user to default role")

    def test_edit_role_not_account_type(self):
        result_info = self.testAdmin.edit_role((self.editTA, self.testAdmin.role.value+1))
        self.assertEqual(result_info['message'], "User can\'t be changed to invalid role\n",
                         msg="Admin was somehow able to change user to invalid role")

    def tearDown(self):
        User.objects.all().delete()

class EditAccountsAsInstructorWithValidData(TestCase):


class EditAccountsAsInstructorWithInvalidData(TestCase):


class EditAccountsAsTAWithValidData(TestCase):


class EditAccountsAsTAWithInvalidData(TestCase):


class DropDownListPopulation(TestCase):