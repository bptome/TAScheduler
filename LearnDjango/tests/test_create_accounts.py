# Create Accounts Unit Tests by Terence Lee
import unittest

import TAInformation.Models.base_user
from TAInformation.Models.admin import UserAdmin
from TAInformation.models import User
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA


# Functions to setup all tests
def all_tests_setup(test_user, id_number: int, name: str, password: str, email: str, address: str, phone: str):
    test_user.user_id = id_number
    test_user.name = name
    test_user.password = password
    test_user.email = email
    test_user.home_address = address
    test_user.phone_number = phone


def setup_database(test_user: TAInformation.Models.base_user.User, test_user_model: User):
    all_tests_setup(test_user_model, test_user.user_id, test_user.name, test_user.password, test_user.email,
                    test_user.home_address, test_user.phone_number)
    test_user_model.save()


class CreateAccountsAsAdmin(unittest.TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testAdmin = UserAdmin()
        all_tests_setup(self.testAdmin,
                        1, "testAdmin", "tA1!", "testAdmin@test.com", "101 W. Wisconsin Ave, Milwaukee, WI 53203",
                        "(414)222-2571")

        # Save to database
        self.an_admin = User()
        setup_database(self.an_admin, self.testAdmin)

    def test_create_admin(self):
        new_admin = UserAdmin()
        all_tests_setup(new_admin, 2, "newAdmin1", "nA1+", "newAdmin1@test.com", "2555 N. Lake Dr, Milwaukee, WI 53201",
                        "(414)224-2018")
        failure_msg = "Couldn\'t create admin account despite having no conflicts"
        self.assertTrue(self.testAdmin.create_admin(new_admin), failure_msg)

    def test_create_instructor(self):
        new_instructor = Instructor()
        all_tests_setup(new_instructor, 3, "firstInstructor", "fI0$", "firstInstructor@test.com",
                        "11111 W. North Ave, Wauwatosa, WI 53219", "(414)445-9870")
        failure_msg = "Couldn\'t create instructor account despite having no conflicts"
        self.assertTrue(self.testAdmin.create_instructor(new_instructor), failure_msg)

    def test_create_ta(self):
        new_ta = TA()
        all_tests_setup(new_ta, 4, "firstTA", "fT7%", "firstTA@test.com", "3814 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)377-0982")
        failure_msg = "Couldn\'t create TA account despite having no conflicts"
        self.assertTrue(self.testAdmin.create_ta(new_ta), failure_msg)

    def tearDown(self):
        User.objects.exclude(id=1).delete()


class CreateAccountsAsInstructor(unittest.TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testInstructor = Instructor()
        all_tests_setup(self.testInstructor, 1, "testInstructor", "tI1!", "testInstructor@test.com",
                        "101 W. Wisconsin Ave, Milwaukee, WI 53203", "(414)222-2571")
        # Save to database
        self.an_instructor = User()
        setup_database(self.testInstructor, self.an_instructor)

    def test_create_admin(self):
        new_admin = UserAdmin()
        all_tests_setup(new_admin, 2, "newAdmin1", "nA1+", "newAdmin1@test.com", "2555 N. Lake Dr, Milwaukee, WI 53201",
                        "(414)224-2018")
        failure_msg = "Created admin account despite not being an admin"
        self.assertFalse(self.testInstructor.create_admin(new_admin), failure_msg)

    def test_create_instructor(self):
        new_instructor = Instructor()
        all_tests_setup(new_instructor, 3, "firstInstructor", "fI0$", "firstInstructor@test.com",
                        "11111 W. North Ave, Wauwatosa, WI 53219", "(414)445-9870")
        failure_msg = "Created instructor account despite not being an admin"
        self.assertFalse(self.testInstructor.create_instructor(new_instructor), failure_msg)

    def test_create_ta(self):
        new_ta = TA()
        all_tests_setup(new_ta, 4, "firstTA", "fT7%", "firstTA@test.com", "3814 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)377-0982")
        failure_msg = "Created TA account despite not being an admin"
        self.assertFalse(self.testInstructor.create_ta(new_ta), failure_msg)

    def tearDown(self):
        User.objects.exclude(id=1).delete()


class CreateAccountsAsTA(unittest.TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testTA = TA()
        all_tests_setup(self.testTA, 1, "testTA", "tT1!", "testTA@test.com",
                        "101 W. Wisconsin Ave, Milwaukee, WI 53203", "(414)222-2571")
        # Save to database
        self.a_ta = User()
        setup_database(self.testTA, self.a_ta)

    def test_create_admin(self):
        new_admin = UserAdmin()
        all_tests_setup(new_admin, 2, "newAdmin1", "nA1+", "newAdmin1@test.com",
                        "2555 N. Lake Dr, Milwaukee, WI 53201", "(414)224-2018")
        failure_msg = "Created admin account despite not being an admin"
        self.assertFalse(self.testTA.create_admin(new_admin), failure_msg)

    def test_create_instructor(self):
        new_instructor = Instructor()
        all_tests_setup(new_instructor, 3, "firstInstructor", "fI0$", "firstInstructor@test.com",
                        "11111 W. North Ave, Wauwatosa, WI 53219", "(414)445-9870")
        failure_msg = "Created instructor account despite not being an admin"
        self.assertFalse(self.testTA.create_instructor(new_instructor), failure_msg)

    def test_create_ta(self):
        new_ta = TA()
        all_tests_setup(new_ta, 4, "firstTA", "fT7%", "firstTA@test.com", "3814 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)377-0982")
        failure_msg = "Created TA account despite not being an admin"
        self.assertFalse(self.testTA.create_ta(new_ta), failure_msg)

    def tearDown(self):
        User.objects.exclude(id=1).delete()


class CheckCredentials(unittest.TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testAdmin = UserAdmin()
        all_tests_setup(self.testAdmin, 1, "testAdmin", "tA1!", "testAdmin@test.com",
                        "101 W. Wisconsin Ave, Milwaukee, WI 53203", "(414)222-2571")
        # Save to database
        self.an_admin = User()
        setup_database(self.testAdmin, self.an_admin)

    def test_NoCredentialsGiven(self):
        test_ta = TA()
        all_tests_setup(test_ta, 2, "", "", "noCred@test.com", "3814 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)444-4444")
        failure_msg = "TA account created despite no credentials given"
        self.assertFalse(self.testAdmin.create_ta(test_ta), failure_msg)

    def test_NoNameBadPassword(self):
        test_ta = TA()
        all_tests_setup(test_ta, 3, "", "password", "noCred2@test.com", "3815 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0001")
        failure_msg = "TA account created with no name and bad password"
        self.assertFalse(self.testAdmin.create_ta(test_ta), failure_msg)

    def test_NoNameGoodPassword(self):
        test_ta = TA()
        all_tests_setup(test_ta, 4, "", "aB3$", "noCred3@test.com", "3816 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0002")
        failure_msg = "TA account created despite no name given"
        self.assertFalse(self.testAdmin.create_ta(test_ta), failure_msg)

    def test_GoodNameNoPassword(self):
        test_ta = TA()
        all_tests_setup(test_ta, 5, "testTA", "", "noCred4@test.com", "3817 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0003")
        failure_msg = "TA account created despite no password given"
        self.assertFalse(self.testAdmin.create_ta(test_ta), failure_msg)

    def test_GoodNameBadPassword(self):
        test_ta = TA()
        all_tests_setup(test_ta, 6, "testTA", "password", "noCred5@test.com",
                        "3818 N. Oakland Ave, Shorewood, WI 53211", "(414)555-0004")
        failure_msg = "TA account created despite bad password given"
        self.assertFalse(self.testAdmin.create_ta(test_ta), failure_msg)

    def test_GoodNameGoodPassword(self):
        test_ta = TA()
        all_tests_setup(test_ta, 7, "testTA", "tA1!", "goodCreds@test.com", "3818 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0004")
        failure_msg = "TA account not created despite good credentials given"
        self.assertTrue(self.testAdmin.create_ta(test_ta), failure_msg)

    def test_BadNameNoPassword(self):
        test_ta = TA()
        all_tests_setup(test_ta, 8, "test", "", "noCred6@test.com", "3819 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0005")
        failure_msg = "TA account created despite bad name and no password given"
        self.assertFalse(self.testAdmin.create_ta(test_ta), failure_msg)

    def test_BadNameBadPassword(self):
        test_ta = TA()
        all_tests_setup(test_ta, 9, "test", "password", "noCred7@test.com", "3820 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0006")
        failure_msg = "TA account created despite bad credentials given"
        self.assertFalse(self.testAdmin.create_ta(test_ta), failure_msg)

    def test_BadNameGoodPassword(self):
        test_ta = TA()
        all_tests_setup(test_ta, 10, "test", "pW4)", "noCred8@test.com", "3821 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0007")
        failure_msg = "TA account created despite bad name given"
        self.assertFalse(self.testAdmin.create_ta(test_ta), failure_msg)

    def tearDown(self):
        User.objects.exclude(id=1).delete()


class CreateDuplicateAccounts(unittest.TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testAdmin = UserAdmin()
        all_tests_setup(self.testAdmin, 1, "testAdmin", "tA1!", "testAdmin@test.com",
                        "101 W. Wisconsin Ave, Milwaukee, WI 53203", "(414)222-2571")
        # Save to database
        self.an_admin = User()
        setup_database(self.testAdmin, self.an_admin)

    def test_CreateExactDuplicate(self):
        failure_msg = "Somehow created a duplicate account"
        self.assertFalse(self.testAdmin.create_admin(self.testAdmin), failure_msg)

    def test_AccountWithDuplicateID(self):
        new_admin = UserAdmin()
        all_tests_setup(new_admin, self.testAdmin.user_id, "testAdmin2", "tA2#", "testAdmin2@test.com",
                        "925 N. MLK Dr, Milwaukee, WI 53203", "(414)555-1001")
        failure_msg = "Created admin account with id already taken"
        self.assertFalse(self.testAdmin.create_admin(new_admin), failure_msg)

    def test_AccountWithDuplicateEmail(self):
        new_admin = UserAdmin()
        all_tests_setup(new_admin, 2, "testAdmin3", "tA3#", self.testAdmin.email, "925 N. MLK Dr, Milwaukee, WI 53203",
                        "(414)555-1001")
        failure_msg = "Created admin account with email already taken"
        self.assertFalse(self.testAdmin.create_admin(new_admin), failure_msg)

    def test_UniqueEmailAndID(self):
        new_admin = self.testAdmin
        all_tests_setup(new_admin, 3, self.testAdmin.name, self.testAdmin.password, "testAdmin4@test.com",
                        self.testAdmin.home_address, self.testAdmin.phone_number)
        failure_msg = "Admin account not created despite unique email and id"
        self.assertTrue(self.testAdmin.create_admin(new_admin), failure_msg)

    def tearDown(self):
        User.objects.exclude(id=1).delete()


class AccountsWithMissingFields(unittest.TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testAdmin = UserAdmin()
        all_tests_setup(self.testAdmin, 1, "testAdmin", "tA1!", "testAdmin@test.com",
                        "101 W. Wisconsin Ave, Milwaukee, WI 53203", "(414)222-2571")
        # Save to database
        self.an_admin = User()
        setup_database(self.testAdmin, self.an_admin)

    def test_MissingID(self):
        new_instructor = Instructor()
        all_tests_setup(new_instructor, None, "testInstructor", "tI5*", "testInstructor@test.com",
                        "2600 N. Humboldt Bd, Milwaukee, WI 53201", "(414)444-7654")
        failure_msg = "Created instructor account despite missing id"
        self.assertFalse(self.testAdmin.create_instructor(new_instructor), failure_msg)

    def test_MissingPassword(self):
        new_instructor = Instructor()
        all_tests_setup(new_instructor, 3, "testInstructor3", None, "testInstructor3@test.com",
                        "2601 N. Humboldt Bd, Milwaukee, WI 53201", "(414)444-7655")
        failure_msg = "Created instructor account despite missing password"
        self.assertFalse(self.testAdmin.create_instructor(new_instructor), failure_msg)

    def test_MissingName(self):
        new_instructor = Instructor()
        all_tests_setup(new_instructor, 4, None, "tI5*", "testInstructor4@test.com",
                        "2602 N. Humboldt Bd, Milwaukee, WI 53201", "(414)444-7656")
        failure_msg = "Created instructor account despite missing name"
        self.assertFalse(self.testAdmin.create_instructor(new_instructor), failure_msg)

    def test_MissingEmail(self):
        new_instructor = Instructor()
        all_tests_setup(new_instructor, 5, "testInstructor5", "tI5*", None, "2603 N. Humboldt Bd, Milwaukee, WI 53201",
                        "(414)444-7657")
        failure_msg = "Created instructor account despite missing email"
        self.assertFalse(self.testAdmin.create_instructor(new_instructor), failure_msg)

    def test_MissingAddress(self):
        new_instructor = Instructor()
        all_tests_setup(new_instructor, 6, "testInstructor6", "tI5*", "testInstructor6@test.com", None, "(414)444-7658")
        failure_msg = "Created instructor account despite missing home address"
        self.assertFalse(self.testAdmin.create_instructor(new_instructor), failure_msg)

    def test_MissingPhoneNumber(self):
        new_instructor = Instructor()
        all_tests_setup(new_instructor, 7, "testInstructor7", "tI5*", "testInstructor7@test.com",
                        "2604 N. Humboldt Bd, Milwaukee, WI 53201", None)
        failure_msg = "Created instructor account despite missing phone number"
        self.assertFalse(self.testAdmin.create_instructor(new_instructor), failure_msg)

    def tearDown(self):
        User.objects.exclude(id=1).delete()
