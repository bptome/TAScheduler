import unittest
import TAInformation.Models.base_user
from TAInformation.Models.admin import UserAdmin
from TAInformation.models import User
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.Models.account_type import AccountType


# Functions to setup all tests

def all_tests_setup(user, Id_number: int, Name: str, Password: str, Email: str, Address: str, Phone: str):
    user.user_id = Id_number
    user.name = Name
    user.password = Password
    user.email = Email
    user.home_address = Address
    user.phone_number = Phone


def setup_database(user: TAInformation.Models.base_user.User, test_user_model: User):
    all_tests_setup(user_model, user.user_id, user.name, user.password, user.email,
                    user.home_address, user.phone_number)
    test_user_model.save()


class test_editAdminUserEmail(unittest.TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testAdmin = UserAdmin()
        all_tests_setup(self.testAdmin,
                        1, "Admin", "Z!", "Admin@test.com", "101 W. Wisconsin Ave, Milwaukee, WI 53203",
                        "(414)222-2571")

        # Save to database
        self.an_admin = User()
        setup_database(self.an_admin, self.testAdmin)

    def test_EditAdminPhoneNUmber(self):
        phoneNumber_admin = UserAdmin()
        all_tests_setup(admin, 1, "Admin", "Z", "Admin1@test.com", "2555 N. Lake Dr, Milwaukee, WI 53201",
                        "(414)111-1111")

        self.assertTrue(self.testAdmin.test_EditAdimnPhoneNUmber(phoneNumber_admin), msg='user Edit his phone number '
                                                                                         'successfully')

    def test_editAdminAddress(self):
        address_admin = UserAdmin()
        all_tests_setup(admin, 1, "Admin", "Z", "Admin1@test.com", "2555 Knap, Milwaukee, WI 53222",
                        "(414)111-1111")

        self.assertTrue(self.testAdmin.test_editAdminAddress(address_admin), msg='user Edit his address successfully')

    def test_editAdminPhoneAndEmail(self):
        PhoneAndEmail_admin = UserAdmin()
        all_tests_setup(admin, 1, "Admin", "Z", "Admin@test.com", "2555 Knap, Milwaukee, WI 53222",
                        "(414)111-2222")

        self.assertTrue(self.testAdmin.test_editAdminPhoneAndEmail(PhoneAndEmail_admin), msg="user Edit his email and "
                                                                                             "phone Number successfully")

    def test_editAdminInformation(self):
        Information_admin = UserAdmin()
        all_tests_setup(admin, 1, "Admin", "Z", "Admin@t.com", "2500 Knap, Milwaukee, WI 53222",
                        "(414)111-2223")

        self.assertTrue(self.testAdmin.test_editAdminInformation(Information_admin), msg="user Edit his information"
                                                                                         "successfully")
