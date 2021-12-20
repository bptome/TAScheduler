# Edit Accounts Unit Tests by: Terence Lee (12/17/2021)
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
        setup_database(self.testAdmin, User())
        self.editTA.save()

    def test_edit_id_to_unused(self):
        result_info = self.testAdmin.edit_user_id(self.editTA, 11)
        self.assertTrue(result_info['result'],
                        msg="User ID wasn\'t changed to 11, despite no user having that ID number")

    def test_edit_id_to_used(self):
        result_info = self.testAdmin.edit_user_id(self.editTA, self.testAdmin.user_id)
        self.assertEqual(result_info['message'],
                         "User with given ID already exists\n",
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
        self.assertEqual(result_info['message'], "User with given email already exists\n",
                         msg="Admin was able to edit user email to one already used by another user")

    def test_edit_password(self):
        result_info = self.testAdmin.edit_password(self.editTA, "gTg1*")
        self.assertTrue(result_info['result'], msg="Admin wasn\'t able to change password to valid password")

    def test_edit_home_address(self):
        result_info = self.testAdmin.edit_home_address(self.editTA, self.testAdmin.home_address)
        self.assertTrue(result_info['result'], msg="Admin wasn\'t able to change user\'s home address to valid address")

    def test_edit_phone_number(self):
        result_info = self.testAdmin.edit_phone(self.editTA, self.testAdmin.phone)
        self.assertTrue(result_info['result'], msg="Admin wasn\'t able to change user\'s phone number to valid number")

    def test_edit_role(self):
        result_info = self.testAdmin.edit_role(self.editTA, AccountType.INSTRUCTOR.value)
        self.assertTrue(result_info['result'], msg="Admin wasn\'t able to change user\'s role to Instructor")

    def tearDown(self):
        User.objects.all().delete()


class EditAccountsAsAdminWithInvalidData(TestCase):
    def setUp(self):
        self.testAdmin = UserAdmin(-1, "", "", "", "", "")
        self.editTA = User(user_id=2, name="Name to be edited later", email="namedlater@test.com", password="p2BNl$",
                           home_address="Address to be edited later", phone="(414)555-9999", role=AccountType.TA.value)
        all_tests_setup(self.testAdmin, 1, "testAdmin", "tA1)", "testAdmin@test.com",
                        "101 E. Wisconsin Ave., Milwaukee, WI 53202", "(414)555-0001")
        setup_database(self.testAdmin, User())
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
       self.assertEqual(result_info['message'], "Invalid name given\n",
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
        result_info = self.testAdmin.edit_role(self.editTA, AccountType.DEFAULT.value)
        self.assertEqual(result_info['message'], "Given role wasn\'t valid\n",
                         msg="Admin was somehow able to change user to default role")

    def test_edit_role_not_account_type(self):
        result_info = self.testAdmin.edit_role(self.editTA, self.testAdmin.role.value+1)
        self.assertEqual(result_info['message'], "Given role wasn\'t valid\n",
                         msg="Admin was somehow able to change user to invalid role")

    def tearDown(self):
        User.objects.all().delete()


class EditAccountsAsInstructorWithValidData(TestCase):
    def setUp(self):
        self.testInstructor = Instructor(-1, "", "", "", "", "")
        self.editTA = User(user_id=2, name="Name to be edited later", email="namedlater@test.com", password="p2BNl$",
                           home_address="Address to be edited later", phone="(414)555-9999", role=AccountType.TA.value)
        all_tests_setup(self.testInstructor, 1, "testInstructor", "tA1)", "testInstructor@test.com",
                        "101 E. Wisconsin Ave., Milwaukee, WI 53202", "(414)555-0001")
        setup_database(self.testInstructor, User())
        self.editTA.save()

    def test_edit_id_other(self):
        result_info = self.testInstructor.edit_user_id(self.editTA, 11)
        self.assertFalse(result_info['result'], msg="User ID was changed to 11, despite editing user not being admin")

    def test_edit_id_self(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_user_id(edit_self, 11)
        self.assertFalse(result_info['result'], msg="User ID was changed to 11, despite editing user not being admin")

    def test_edit_name_other(self):
        result_info = self.testInstructor.edit_name(self.editTA, "editTA")
        self.assertFalse(result_info['result'],
                         msg="User was able to change another user\'s name despite being not being an admin")

    def test_edit_name_self(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_name(edit_self, "editInstructor")
        self.assertFalse(result_info['result'],
                         msg="User was able to change their name despite being not being an admin")

    def test_edit_email_other(self):
        result_info = self.testInstructor.edit_email(self.editTA, "editTA@test.com")
        self.assertFalse(result_info['result'],
                        msg="User was able to change email despite not being an admin")

    def test_edit_email_self_taken(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_email(edit_self, self.editTA.email)
        self.assertFalse(result_info['result'],
                         msg="Instructor was able to use email already taken")

    def test_edit_email_self_free(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_email(edit_self, "editInstructor@test.com")
        self.assertTrue(result_info['result'],
                         msg="Instructor wasn\'t able to use valid email that no other user had")

    def test_edit_password_other(self):
        result_info = self.testInstructor.edit_password(self.editTA, "gTg1*")
        self.assertFalse(result_info['result'],
                         msg="Instructor was able to change other user\'s password despite not being an admin")

    def test_edit_password_self(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_password(edit_self, "g!1G")
        self.assertTrue(result_info['result'], msg="Instructor wasn\'t able to change their password to a valid one")

    def test_edit_home_address_other(self):
        result_info = self.testInstructor.edit_home_address(self.editTA, self.testInstructor.home_address)
        self.assertFalse(result_info['result'],
                         msg="Instructor was able to change other user\'s home address to valid address despite not being an admin")

    def test_edit_home_address_self(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_home_address(edit_self, "2200 E. Kenwood Bd., Milwaukee, WI 53201")
        self.assertTrue(result_info['result'],
                         msg="Instructor wasn\'t able to change their home address to valid address")

    def test_edit_phone_number_other(self):
        result_info = self.testInstructor.edit_phone(self.editTA, self.testInstructor.phone)
        self.assertFalse(result_info['result'],
                         msg="Instructor was able to change other user\'s phone number to valid number despite being non-admin account")

    def test_edit_phone_number_self(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_phone(edit_self, self.editTA.phone)
        self.assertTrue(result_info['result'],
                         msg="Instructor wasn\'t able to change their phone number to valid number")

    def test_edit_role_other(self):
        result_info = self.testInstructor.edit_role(self.editTA, AccountType.INSTRUCTOR.value)
        self.assertFalse(result_info['result'],
                         msg="Instructor was able to change other user\'s role despite being non-admin account")

    def test_edit_role_self(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_role(edit_self, AccountType.ADMIN.value)
        self.assertFalse(result_info['result'],
                         msg="Instructor was able to change their role despite being non-admin account")

    def tearDown(self):
        User.objects.all().delete()


class EditAccountsAsInstructorWithInvalidData(TestCase):
    def setUp(self):
        self.testInstructor = Instructor(-1, "", "", "", "", "")
        self.editTA = User(user_id=2, name="Name to be edited later", email="namedlater@test.com", password="p2BNl$",
                           home_address="Address to be edited later", phone="(414)555-9999", role=AccountType.TA.value)
        all_tests_setup(self.testInstructor, 1, "testInstructor", "tA1)", "testInstructor@test.com",
                        "101 E. Wisconsin Ave., Milwaukee, WI 53202", "(414)555-0001")
        setup_database(self.testInstructor, User())
        self.editTA.save()

    def test_edit_user_id_other(self):
        result_info = self.testInstructor.edit_user_id(self.editTA, -1)
        self.assertFalse(result_info['result'],
                         msg="Instructor was able to change other user's ID despite being an non-admin account")

    def test_edit_user_id_self_neg(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_user_id(edit_self, -1)
        self.assertFalse(result_info['result'],
                         msg="Instructor was able to change their ID to negative value")

    def test_edit_user_id_self_blank(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_user_id(edit_self, "")
        self.assertFalse(result_info['result'],
                         msg="Instructor was able to change their ID to blank string")

    def test_edit_name_other(self):
        result_info = self.testInstructor.edit_name(self.editTA, "name")
        self.assertEqual(result_info['message'], 'Only admins can change names\n',
                         msg="Instructor was able to change other user\'s name to one that\'s too short")

    def test_edit_name_self(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_name(edit_self, "name")
        self.assertEqual(result_info['message'], 'Only admins can change names\n',
                         msg="Instructor was able to change their name to one that\'s too short")

    def test_edit_email_self(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_email(edit_self, "test.com")
        self.assertFalse(result_info['result'],
                         msg="Instructor\'s invalid email wasn\'t caught by validator")

    def test_edit_email_other(self):
        result_info = self.testInstructor.edit_email(self.editTA, "test.com")
        self.assertFalse(result_info['result'],
                         msg="Instructor\'s invalid email wasn\'t caught by validator")

    def test_edit_password_self_too_short(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_password(edit_self, "gTg")
        self.assertEqual(result_info['message'], "Password must be at least 4 characters long\n",
                         msg="Instructor was able to change their password to one shorter than the minimum length")

    def test_edit_password_self_missing_uppercase(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_password(edit_self, "g1&g")
        self.assertEqual(result_info['message'], "Password must contain >= 1 uppercase letter\n",
                         msg="Instructor was able to change their password to one without uppercase letter")

    def test_edit_password_self_missing_lowercase(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_password(edit_self, "G1&G")
        self.assertEqual(result_info['message'], "Password must contain >= 1 lowercase letter\n",
                         msg="Instructor was able to change their password to one without lowercase letter")

    def test_edit_password_self_missing_number(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_password(edit_self, "G!&g")
        self.assertEqual(result_info['message'], "Password must contain >= 1 number\n",
                         msg="Instructor was able to change their password to one without a number")

    def test_edit_password_self_missing_special(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_password(edit_self, "g18G")
        self.assertEqual(result_info['message'], "Password must contain >= 1 non-alphanumeric character\n",
                         msg="Instructor was able to change their password to one without non-alphanumeric character")

    def test_edit_password_other_too_short(self):
        result_info = self.testInstructor.edit_password(self.editTA, "gTg")
        self.assertEqual(result_info['message'], "Instructors can only edit their own password\n",
                         msg="Instructor was able to change their password to one shorter than the minimum length")

    def test_edit_password_other_missing_uppercase(self):
        result_info = self.testInstructor.edit_password(self.editTA, "g1&g")
        self.assertEqual(result_info['message'], "Instructors can only edit their own password\n",
                         msg="Instructor was able to change their password to one without uppercase letter")

    def test_edit_password_other_missing_lowercase(self):
        result_info = self.testInstructor.edit_password(self.editTA, "G1&G")
        self.assertEqual(result_info['message'], "Instructors can only edit their own password\n",
                         msg="Instructor was able to change their password to one without lowercase letter")

    def test_edit_password_other_missing_number(self):
        result_info = self.testInstructor.edit_password(self.editTA, "G!&g")
        self.assertEqual(result_info['message'], "Instructors can only edit their own password\n",
                         msg="Instructor was able to change their password to one without a number")

    def test_edit_password_other_missing_special(self):
        result_info = self.testInstructor.edit_password(self.editTA, "g18G")
        self.assertEqual(result_info['message'], "Instructors can only edit their own password\n",
                         msg="Instructor was able to change their password to one without non-alphanumeric character")

    def test_edit_home_address_other_blank(self):
        result_info = self.testInstructor.edit_home_address(self.editTA, "")
        self.assertEqual(result_info['message'], 'Instructors can only edit their own home address\n',
                         msg="Instructor was able to change other user\'s home address to an empty string")

    def test_edit_home_address_self_blank(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_home_address(edit_self, "")
        self.assertEqual(result_info['message'], "Home address is missing\n",
                         msg="Instructor was able to change their home address to an empty string")

    def test_edit_home_address_other_spaces(self):
        result_info = self.testInstructor.edit_home_address(self.editTA, "  ")
        self.assertEqual(result_info['message'], 'Instructors can only edit their own home address\n',
                         msg="Instructor was able to change other user\'s home address to a string with only spaces in it")

    def test_edit_home_address_self_spaces(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_home_address(edit_self, "  ")
        self.assertEqual(result_info['message'], "Home address must contain some non-space characters\n",
                         msg="Instructor was able to change their home address to a string with only spaces in it")

    def test_edit_phone_other_blank(self):
        result_info = self.testInstructor.edit_phone(self.editTA, "")
        self.assertEqual(result_info['message'], 'Instructors can only edit their own phone number\n',
                         msg="Instructor was able to change other user\'s phone number to an empty string")

    def test_edit_phone_self_blank(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_phone(edit_self, "")
        self.assertEqual(result_info['message'], "No phone number given\n",
                         msg="Instructor was able to change their phone number to an empty string")

    def test_edit_phone_other_wrong_amount(self):
        result_info = self.testInstructor.edit_phone(self.editTA, "4145550123")
        self.assertEqual(result_info['message'], 'Instructors can only edit their own phone number\n',
                         msg="Instructor was able to change other user\'s phone number to an string that doesn\'t have exactly 13 characters")

    def test_edit_phone_self_wrong_amount(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_phone(edit_self, "4145550123")
        self.assertEqual(result_info['message'], "Phone number should have exactly 13 characters\n",
                         msg="Instructor was able to change other user\'s phone number to an string that doesn\'t have exactly 13 characters")

    def test_edit_phone_other_misplaced(self):
        result_info = self.testInstructor.edit_phone(self.editTA, "(414)A55-0123")
        self.assertEqual(result_info['message'], 'Instructors can only edit their own phone number\n',
                         msg="Instructor was able to change other user\'s phone number to one that has a non-digit in a place that one is expected")

    def test_edit_phone_self_misplaced(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_phone(edit_self, "(414)A55-0123")
        self.assertEqual(result_info['message'], "Misplaced character in phone number entry\n",
                         msg="Instructor was able to change their phone number to one that has a non-digit in a place that one is expected")

    def test_edit_phone_other_lead_parentheses(self):
        result_info = self.testInstructor.edit_phone(self.editTA, "1414)555-0123")
        self.assertEqual(result_info['message'], 'Instructors can only edit their own phone number\n',
                         msg="Instructor was able to change other user\'s phone number to one that doesn\'t have a lead parentheses")

    def test_edit_phone_self_lead_parentheses(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_phone(edit_self, "1414)555-0123")
        self.assertEqual(result_info['message'], "Missing lead parentheses in phone number entry\n",
                         msg="Instructor was able to change their phone number to one that doesn\'t have a lead parentheses")

    def test_edit_phone_other_trail_parentheses(self):
        result_info = self.testInstructor.edit_phone(self.editTA, "(4141555-0123")
        self.assertEqual(result_info['message'], 'Instructors can only edit their own phone number\n',
                         msg="Instructor was able to change other user\'s phone number to one that doesn\'t have a trailing parentheses in its expected place")

    def test_edit_phone_self_trail_parentheses(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_phone(edit_self, "(4141555-0123")
        self.assertEqual(result_info['message'], "Missing trailing parentheses in phone number entry\n",
                         msg="Instructor was able to change their phone number to one that doesn\'t have a trailing parentheses in its expected place")

    def test_edit_phone_other_dash(self):
        result_info = self.testInstructor.edit_phone(self.editTA, "(414)55510123")
        self.assertEqual(result_info['message'], 'Instructors can only edit their own phone number\n',
                         msg="Instructor was able to change other user\'s phone number to one that doesn\'t have a dash in its expected place")

    def test_edit_phone_self_dash(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_phone(edit_self, "(414)55510123")
        self.assertEqual(result_info['message'], "Missing dash between prefix and suffix in phone number entry\n",
                         msg="Instructor was able to change their phone number to one that doesn\'t have a dash in its expected place")

    def test_edit_role_other_default(self):
        result_info = self.testInstructor.edit_role(self.editTA, AccountType.DEFAULT.value)
        self.assertEqual(result_info['message'], "Instructors can\'t change anyone\'s role\n",
                         msg="Instructor was somehow able to change other user to default role")

    def test_edit_role_self_default(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_role(edit_self, AccountType.DEFAULT.value)
        self.assertEqual(result_info['message'], "Instructors can\'t change anyone\'s role\n",
                         msg="Instructor was somehow able to change themselves to default role")

    def test_edit_role_other_not_account_type(self):
        result_info = self.testInstructor.edit_role(self.editTA, self.testInstructor.role.value+1)
        self.assertEqual(result_info['message'], "Instructors can\'t change anyone\'s role\n",
                         msg="Instructor was somehow able to change other user to invalid role")

    def test_edit_role_self_not_account_type(self):
        edit_self = User.objects.get(user_id=self.testInstructor.user_id)
        result_info = self.testInstructor.edit_role(edit_self, self.testInstructor.role.value+1)
        self.assertEqual(result_info['message'], "Instructors can\'t change anyone\'s role\n",
                         msg="Instructor was somehow able to change themselves to invalid role")

    def tearDown(self):
        User.objects.all().delete()


class EditAccountsAsTAWithValidData(TestCase):
    def setUp(self):
        self.testTA = TA(-1, "", "", "", "", "")
        self.editTA = User(user_id=2, name="Name to be edited later", email="namedlater@test.com", password="p2BNl$",
                           home_address="Address to be edited later", phone="(414)555-9999", role=AccountType.TA.value)
        all_tests_setup(self.testTA, 1, "testTA", "tA1)", "testTA@test.com",
                        "101 E. Wisconsin Ave., Milwaukee, WI 53202", "(414)555-0001")
        setup_database(self.testTA, User())
        self.editTA.save()

    def test_edit_id_other(self):
        result_info = self.testTA.edit_user_id(self.editTA, 11)
        self.assertFalse(result_info['result'], msg="User ID was changed to 11, despite editing user not being admin")

    def test_edit_id_self(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_user_id(edit_self, 11)
        self.assertFalse(result_info['result'], msg="User ID was changed to 11, despite editing user not being admin")

    def test_edit_name_other(self):
        result_info = self.testTA.edit_name(self.editTA, "editTA")
        self.assertFalse(result_info['result'],
                         msg="TA was able to change another user\'s name despite being not being an admin")

    def test_edit_name_self(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_name(edit_self, "editInstructor")
        self.assertFalse(result_info['result'],
                         msg="TA was able to change their name despite being not being an admin")

    def test_edit_email_other(self):
        result_info = self.testTA.edit_email(self.editTA, "editTA@test.com")
        self.assertFalse(result_info['result'],
                         msg="TA was able to change email despite not being an admin")

    def test_edit_email_self_taken(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_email(edit_self, self.editTA.email)
        self.assertFalse(result_info['result'],
                         msg="TA was able to use email already taken")

    def test_edit_email_self_free(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_email(edit_self, "editInstructor@test.com")
        self.assertTrue(result_info['result'],
                        msg="TA wasn\'t able to use valid email that no other user had")

    def test_edit_password_other(self):
        result_info = self.testTA.edit_password(self.editTA, "gTg1*")
        self.assertFalse(result_info['result'],
                         msg="TA was able to change other user\'s password despite not being an admin")

    def test_edit_password_self(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_password(edit_self, "g!1G")
        self.assertTrue(result_info['result'], msg="TA wasn\'t able to change their password to a valid one")

    def test_edit_home_address_other(self):
        result_info = self.testTA.edit_home_address(self.editTA, self.testTA.home_address)
        self.assertFalse(result_info['result'],
                         msg="TA was able to change other user\'s home address to valid address despite not being an admin")

    def test_edit_home_address_self(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_home_address(edit_self, "2200 E. Kenwood Bd., Milwaukee, WI 53201")
        self.assertTrue(result_info['result'],
                        msg="TA wasn\'t able to change their home address to valid address")

    def test_edit_phone_number_other(self):
        result_info = self.testTA.edit_phone(self.editTA, self.testTA.phone)
        self.assertFalse(result_info['result'],
                         msg="TA was able to change other user\'s phone number to valid number despite being non-admin account")

    def test_edit_phone_number_self(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_phone(edit_self, self.editTA.phone)
        self.assertTrue(result_info['result'],
                         msg="TA wasn\'t able to change their phone number to valid number")

    def test_edit_role_other(self):
        result_info = self.testTA.edit_role(self.editTA, AccountType.INSTRUCTOR)
        self.assertFalse(result_info['result'],
                         msg="TA was able to change other user\'s role despite being non-admin account")

    def test_edit_role_self(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_role(edit_self, AccountType.ADMIN)
        self.assertFalse(result_info['result'],
                         msg="TA was able to change their role despite being non-admin account")

    def tearDown(self):
        User.objects.all().delete()


class EditAccountsAsTAWithInvalidData(TestCase):
    def setUp(self):
        self.testTA = TA(-1, "", "", "", "", "")
        self.editTA = User(user_id=2, name="Name to be edited later", email="namedlater@test.com", password="p2BNl$",
                           home_address="Address to be edited later", phone="(414)555-9999", role=AccountType.TA.value)
        all_tests_setup(self.testTA, 1, "testTA", "tA1)", "testTA@test.com",
                        "101 E. Wisconsin Ave., Milwaukee, WI 53202", "(414)555-0001")
        setup_database(self.testTA, User())
        self.editTA.save()

    def test_edit_user_id_other(self):
        result_info = self.testTA.edit_user_id(self.editTA, -1)
        self.assertFalse(result_info['result'],
                         msg="TA was able to change other user's ID despite being an non-admin account")

    def test_edit_user_id_self_neg(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_user_id(edit_self, -1)
        self.assertFalse(result_info['result'],
                         msg="TA was able to change their ID to negative value")

    def test_edit_user_id_self_blank(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_user_id(edit_self, "")
        self.assertFalse(result_info['result'],
                         msg="TA was able to change their ID to blank string")

    def test_edit_name_other(self):
        result_info = self.testTA.edit_name(self.editTA, "name")
        self.assertEqual(result_info['message'], "Only admins can change names\n",
                         msg="TA was able to change other user\'s name to one that\'s too short")

    def test_edit_name_self(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_name(edit_self, "name")
        self.assertEqual(result_info['message'], "Only admins can change names\n",
                         msg="TA was able to change their name to one that\'s too short")

    def test_edit_email_self(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_email(edit_self, "test.com")
        self.assertFalse(result_info['result'],
                         msg="TA\'s invalid email wasn\'t caught by validator")

    def test_edit_email_other(self):
        result_info = self.testTA.edit_email(self.editTA, "test.com")
        self.assertFalse(result_info['result'],
                         msg="TA\'s invalid email wasn\'t caught by validator")

    def test_edit_password_self_too_short(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_password(edit_self, "gTg")
        self.assertEqual(result_info['message'], "Password must be at least 4 characters long\n",
                         msg="TA was able to change their password to one shorter than the minimum length")

    def test_edit_password_self_missing_uppercase(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_password(edit_self, "g1&g")
        self.assertEqual(result_info['message'], "Password must contain >= 1 uppercase letter\n",
                         msg="TA was able to change their password to one without uppercase letter")

    def test_edit_password_self_missing_lowercase(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_password(edit_self, "G1&G")
        self.assertEqual(result_info['message'], "Password must contain >= 1 lowercase letter\n",
                         msg="TA was able to change their password to one without lowercase letter")

    def test_edit_password_self_missing_number(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_password(edit_self, "G!&g")
        self.assertEqual(result_info['message'], "Password must contain >= 1 number\n",
                         msg="TA was able to change their password to one without a number")

    def test_edit_password_self_missing_special(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_password(edit_self, "g18G")
        self.assertEqual(result_info['message'], "Password must contain >= 1 non-alphanumeric character\n",
                         msg="TA was able to change their password to one without non-alphanumeric character")

    def test_edit_password_other_too_short(self):
        result_info = self.testTA.edit_password(self.editTA, "gTg")
        self.assertEqual(result_info['message'], "TAs can only edit their own password\n",
                         msg="TA was able to change their password to one shorter than the minimum length")

    def test_edit_password_other_missing_uppercase(self):
        result_info = self.testTA.edit_password(self.editTA, "g1&g")
        self.assertEqual(result_info['message'], "TAs can only edit their own password\n",
                         msg="TA was able to change their password to one without uppercase letter")

    def test_edit_password_other_missing_lowercase(self):
        result_info = self.testTA.edit_password(self.editTA, "G1&G")
        self.assertEqual(result_info['message'], "TAs can only edit their own password\n",
                         msg="TA was able to change their password to one without lowercase letter")

    def test_edit_password_other_missing_number(self):
        result_info = self.testTA.edit_password(self.editTA, "G!&g")
        self.assertEqual(result_info['message'], "TAs can only edit their own password\n",
                         msg="TA was able to change their password to one without a number")

    def test_edit_password_other_missing_special(self):
        result_info = self.testTA.edit_password(self.editTA, "g18G")
        self.assertEqual(result_info['message'], "TAs can only edit their own password\n",
                         msg="TA was able to change their password to one without non-alphanumeric character")

    def test_edit_home_address_other_blank(self):
        result_info = self.testTA.edit_home_address(self.editTA, "")
        self.assertEqual(result_info['message'], "TAs can only edit their own home address\n",
                         msg="TA was able to change other user\'s home address to an empty string")

    def test_edit_home_address_self_blank(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_home_address(edit_self, "")
        self.assertEqual(result_info['message'], "Home address is missing\n",
                         msg="TA was able to change their home address to an empty string")

    def test_edit_home_address_other_spaces(self):
        result_info = self.testTA.edit_home_address(self.editTA, "  ")
        self.assertEqual(result_info['message'], "TAs can only edit their own home address\n",
                         msg="TA was able to change other user\'s home address to a string with only spaces in it")

    def test_edit_home_address_self_spaces(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_home_address(edit_self, "  ")
        self.assertEqual(result_info['message'], "Home address must contain some non-space characters\n",
                         msg="TA was able to change their home address to a string with only spaces in it")

    def test_edit_phone_other_blank(self):
        result_info = self.testTA.edit_phone(self.editTA, "")
        self.assertEqual(result_info['message'], "TAs can only edit their own phone number\n",
                         msg="TA was able to change other user\'s phone number to an empty string")

    def test_edit_phone_self_blank(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_phone(edit_self, "")
        self.assertEqual(result_info['message'], "No phone number given\n",
                         msg="TA was able to change their phone number to an empty string")

    def test_edit_phone_other_wrong_amount(self):
        result_info = self.testTA.edit_phone(self.editTA, "4145550123")
        self.assertEqual(result_info['message'], "TAs can only edit their own phone number\n",
                         msg="TA was able to change other user\'s phone number to an string that doesn\'t have exactly 13 characters")

    def test_edit_phone_self_wrong_amount(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_phone(edit_self, "4145550123")
        self.assertEqual(result_info['message'], "Phone number should have exactly 13 characters\n",
                         msg="TA was able to change other user\'s phone number to an string that doesn\'t have exactly 13 characters")

    def test_edit_phone_other_misplaced(self):
        result_info = self.testTA.edit_phone(self.editTA, "(414)A55-0123")
        self.assertEqual(result_info['message'], "TAs can only edit their own phone number\n",
                         msg="TA was able to change other user\'s phone number to one that has a non-digit in a place that one is expected")

    def test_edit_phone_self_misplaced(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_phone(edit_self, "(414)A55-0123")
        self.assertEqual(result_info['message'], "Misplaced character in phone number entry\n",
                         msg="TA was able to change their phone number to one that has a non-digit in a place that one is expected")

    def test_edit_phone_other_lead_parentheses(self):
        result_info = self.testTA.edit_phone(self.editTA, "1414)555-0123")
        self.assertEqual(result_info['message'], "TAs can only edit their own phone number\n",
                         msg="TA was able to change other user\'s phone number to one that doesn\'t have a lead parentheses")

    def test_edit_phone_self_lead_parentheses(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_phone(edit_self, "1414)555-0123")
        self.assertEqual(result_info['message'], "Missing lead parentheses in phone number entry\n",
                         msg="TA was able to change their phone number to one that doesn\'t have a lead parentheses")

    def test_edit_phone_other_trail_parentheses(self):
        result_info = self.testTA.edit_phone(self.editTA, "(4141555-0123")
        self.assertEqual(result_info['message'], "TAs can only edit their own phone number\n",
                         msg="TA was able to change other user\'s phone number to one that doesn\'t have a trailing parentheses in its expected place")

    def test_edit_phone_self_trail_parentheses(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_phone(edit_self, "(4141555-0123")
        self.assertEqual(result_info['message'], "Missing trailing parentheses in phone number entry\n",
                         msg="TA was able to change their phone number to one that doesn\'t have a trailing parentheses in its expected place")

    def test_edit_phone_other_dash(self):
        result_info = self.testTA.edit_phone(self.editTA, "(414)55510123")
        self.assertEqual(result_info['message'], "TAs can only edit their own phone number\n",
                         msg="TA was able to change other user\'s phone number to one that doesn\'t have a dash in its expected place")

    def test_edit_phone_self_dash(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_phone(edit_self, "(414)55510123")
        self.assertEqual(result_info['message'], "Missing dash between prefix and suffix in phone number entry\n",
                         msg="TA was able to change their phone number to one that doesn\'t have a dash in its expected place")

    def test_edit_role_other_default(self):
        result_info = self.testTA.edit_role(self.editTA, AccountType.DEFAULT.value)
        self.assertEqual(result_info['message'], "TAs can\'t change anyone\'s role\n",
                         msg="TA was somehow able to change other user to default role")

    def test_edit_role_self_default(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_role(edit_self, AccountType.DEFAULT.value)
        self.assertEqual(result_info['message'], "TAs can\'t change anyone\'s role\n",
                         msg="TA was somehow able to change themselves to default role")

    def test_edit_role_other_not_account_type(self):
        result_info = self.testTA.edit_role(self.editTA, self.testTA.role.value+3)
        self.assertEqual(result_info['message'], "TAs can\'t change anyone\'s role\n",
                         msg="TA was somehow able to change other user to invalid role")

    def test_edit_role_self_not_account_type(self):
        edit_self = User.objects.get(user_id=self.testTA.user_id)
        result_info = self.testTA.edit_role(edit_self, self.testTA.role.value+3)
        self.assertEqual(result_info['message'], "TAs can\'t change anyone\'s role\n",
                         msg="TA was somehow able to change themselves to invalid role")

    def tearDown(self):
        User.objects.all().delete()


class DropDownListPopulation(TestCase):
    def setUp(self):
        self.listedAdmin = User(user_id=1, name="listedAdmin", email="listedAdmin@test.com", password="p2BNl$",
                                home_address="Address to be edited later", phone="(414)555-9999",
                                role=AccountType.ADMIN.value)
        self.listedInstructor = User(user_id=2, name="listedInstructor", email="listedInstructor@test.com",
                                     password="p2BNl$", home_address="Address to be edited later",
                                     phone="(414)555-9999", role=AccountType.INSTRUCTOR.value)
        self.listedTA = User(user_id=3, name="listedTA", email="listedTA@test.com", password="p2BNl$",
                             home_address="Address to be edited later", phone="(414)555-9999",
                             role=AccountType.TA.value)
        self.listedAdmin.save()
        self.listedInstructor.save()
        self.listedTA.save()

    def test_dropdown_as_admin(self):
        test_admin = UserAdmin(id_number=self.listedAdmin.user_id, name=self.listedAdmin.name,
                               email=self.listedAdmin.email, password=self.listedAdmin.password,
                               address=self.listedAdmin.home_address, phone=self.listedAdmin.phone)
        actual_list = test_admin.list_of_editable_users()
        expected_list = [self.listedAdmin, self.listedInstructor, self.listedTA]
        self.assertEqual(actual_list, expected_list, msg="Editable user lists didn\'t load up all users in database")

    def test_dropdown_as_instructor(self):
        test_instructor = Instructor(id_number=self.listedInstructor.user_id, name=self.listedInstructor.name,
                                     email=self.listedInstructor.email, password=self.listedInstructor.password,
                                     address=self.listedInstructor.home_address, phone=self.listedInstructor.phone)
        actual_list = test_instructor.list_of_editable_users()
        expected_list = [self.listedInstructor]
        self.assertEqual(actual_list, expected_list, msg="Editable user lists didn\'t just consist of the calling user")

    def test_dropdown_as_ta(self):
        test_ta = TA(id_number=self.listedTA.user_id, name=self.listedTA.name, email=self.listedTA.email,
                     password=self.listedTA.password, address=self.listedTA.home_address, phone=self.listedTA.phone)
        actual_list = test_ta.list_of_editable_users()
        expected_list = [self.listedTA]
        self.assertEqual(actual_list, expected_list, msg="Editable user lists didn\'t just consist of the calling user")
