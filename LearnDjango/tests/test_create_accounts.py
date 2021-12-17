# Create Accounts Unit Tests by Terence Lee
from django.test import TestCase
from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.validator_methods import all_tests_setup, setup_database
from TAInformation.models import User
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA


class CreateAccountsAsAdmin(TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testAdmin = UserAdmin(-1, "", "", "", "", "")
        all_tests_setup(self.testAdmin,
                        1, "testAdmin", "tA1!", "testAdmin@test.com", "101 W. Wisconsin Ave, Milwaukee, WI 53203",
                        "(414)222-2571")

        # Save to database
        self.an_admin = User(user_id=-1, name="", password="", email="", home_address="", phone="", role=0)
        setup_database(self.testAdmin, self.an_admin)

    def test_create_admin(self):
        new_admin = UserAdmin(-1, "", "", "", "", "")
        all_tests_setup(new_admin, 2, "newAdmin1", "nA1+", "newAdmin1@test.com", "2555 N. Lake Dr, Milwaukee, WI 53201",
                        "(414)224-2018")
        failure_msg = "Couldn\'t create admin account despite having no conflicts"
        result_pkg = self.testAdmin.create_user(new_admin)
        self.assertTrue(result_pkg['result'], failure_msg)

    def test_create_instructor(self):
        new_instructor = Instructor(-1, "", "", "", "", "")
        all_tests_setup(new_instructor, 3, "firstInstructor", "fI0$", "firstInstructor@test.com",
                        "11111 W. North Ave, Wauwatosa, WI 53219", "(414)445-9870")
        failure_msg = "Couldn\'t create instructor account despite having no conflicts"
        result_pkg = self.testAdmin.create_user(new_instructor)
        self.assertTrue(result_pkg['result'], failure_msg)

    def test_create_ta(self):
        new_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(new_ta, 4, "firstTA", "fT7%", "firstTA@test.com", "3814 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)377-0982")
        failure_msg = "Couldn\'t create TA account despite having no conflicts"
        result_pkg = self.testAdmin.create_user(new_ta)
        self.assertTrue(result_pkg['result'], failure_msg)

    def tearDown(self):
        User.objects.exclude(user_id=1).delete()


class CreateAccountsAsInstructor(TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testInstructor = Instructor(-1, "", "", "", "", "")
        all_tests_setup(self.testInstructor, 1, "testInstructor", "tI1!", "testInstructor@test.com",
                        "101 W. Wisconsin Ave, Milwaukee, WI 53203", "(414)222-2571")
        # Save to database
        self.an_instructor = User()
        setup_database(self.testInstructor, self.an_instructor)

    def test_create_admin(self):
        new_admin = UserAdmin(-1, "", "", "", "", "")
        all_tests_setup(new_admin, 2, "newAdmin1", "nA1+", "newAdmin1@test.com", "2555 N. Lake Dr, Milwaukee, WI 53201",
                        "(414)224-2018")
        failure_msg = "Created admin account despite not being an admin"
        result_pkg = self.testInstructor.create_user(new_admin)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_create_instructor(self):
        new_instructor = Instructor(-1, "", "", "", "", "")
        all_tests_setup(new_instructor, 3, "firstInstructor", "fI0$", "firstInstructor@test.com",
                        "11111 W. North Ave, Wauwatosa, WI 53219", "(414)445-9870")
        failure_msg = "Created instructor account despite not being an admin"
        result_pkg = self.testInstructor.create_user(new_instructor)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_create_ta(self):
        new_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(new_ta, 4, "firstTA", "fT7%", "firstTA@test.com", "3814 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)377-0982")
        failure_msg = "Created TA account despite not being an admin"
        result_pkg = self.testInstructor.create_user(new_ta)
        self.assertFalse(result_pkg['result'], failure_msg)

    def tearDown(self):
        User.objects.exclude(user_id=1).delete()


class CreateAccountsAsTA(TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testTA = TA(-1, "", "", "", "", "")
        all_tests_setup(self.testTA, 1, "testTA", "tT1!", "testTA@test.com",
                        "101 W. Wisconsin Ave, Milwaukee, WI 53203", "(414)222-2571")
        # Save to database
        self.a_ta = User()
        setup_database(self.testTA, self.a_ta)

    def test_create_admin(self):
        new_admin = UserAdmin(-1, "", "", "", "", "")
        all_tests_setup(new_admin, 2, "newAdmin1", "nA1+", "newAdmin1@test.com",
                        "2555 N. Lake Dr, Milwaukee, WI 53201", "(414)224-2018")
        failure_msg = "Created admin account despite not being an admin"
        result_pkg = self.testTA.create_user(new_admin)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_create_instructor(self):
        new_instructor = Instructor(-1, "", "", "", "", "")
        all_tests_setup(new_instructor, 3, "firstInstructor", "fI0$", "firstInstructor@test.com",
                        "11111 W. North Ave, Wauwatosa, WI 53219", "(414)445-9870")
        failure_msg = "Created instructor account despite not being an admin"
        result_pkg = self.testTA.create_user(new_instructor)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_create_ta(self):
        new_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(new_ta, 4, "firstTA", "fT7%", "firstTA@test.com", "3814 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)377-0982")
        failure_msg = "Created TA account despite not being an admin"
        result_pkg = self.testTA.create_user(new_ta)
        self.assertFalse(result_pkg['result'], failure_msg)

    def tearDown(self):
        User.objects.exclude(user_id=1).delete()


class CheckCredentials(TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testAdmin = UserAdmin(-1, "", "", "", "", "")
        all_tests_setup(self.testAdmin, 1, "testAdmin", "tA1!", "testAdmin@test.com",
                        "101 W. Wisconsin Ave, Milwaukee, WI 53203", "(414)222-2571")
        # Save to database
        self.an_admin = User()
        setup_database(self.testAdmin, self.an_admin)

    def test_NoCredentialsGiven(self):
        test_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(test_ta, 2, "", "", "noCred@test.com", "3814 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)444-4444")
        failure_msg = "TA account created despite no credentials given"
        result_pkg = self.testAdmin.create_user(test_ta)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_NoNameBadPassword(self):
        test_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(test_ta, 3, "", "password", "noCred2@test.com", "3815 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0001")
        failure_msg = "TA account created with no name and bad password"
        result_pkg = self.testAdmin.create_user(test_ta)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_NoNameGoodPassword(self):
        test_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(test_ta, 4, "", "aB3$", "noCred3@test.com", "3816 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0002")
        failure_msg = "TA account created despite no name given"
        result_pkg = self.testAdmin.create_user(test_ta)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_GoodNameNoPassword(self):
        test_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(test_ta, 5, "testTA", "", "noCred4@test.com", "3817 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0003")
        failure_msg = "TA account created despite no password given"
        result_pkg = self.testAdmin.create_user(test_ta)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_GoodNameBadPassword(self):
        test_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(test_ta, 6, "testTA", "password", "noCred5@test.com",
                        "3818 N. Oakland Ave, Shorewood, WI 53211", "(414)555-0004")
        failure_msg = "TA account created despite bad password given"
        result_pkg = self.testAdmin.create_user(test_ta)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_GoodNameGoodPassword(self):
        test_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(test_ta, 7, "testTA", "tA1!", "goodCreds@test.com", "3818 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0004")
        failure_msg = "TA account not created despite good credentials given"
        result_pkg = self.testAdmin.create_user(test_ta)
        self.assertTrue(result_pkg['result'], failure_msg)

    def test_BadNameNoPassword(self):
        test_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(test_ta, 8, "test", "", "noCred6@test.com", "3819 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0005")
        failure_msg = "TA account created despite bad name and no password given"
        result_pkg = self.testAdmin.create_user(test_ta)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_BadNameBadPassword(self):
        test_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(test_ta, 9, "test", "password", "noCred7@test.com", "3820 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0006")
        failure_msg = "TA account created despite bad credentials given"
        result_pkg = self.testAdmin.create_user(test_ta)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_BadNameGoodPassword(self):
        test_ta = TA(-1, "", "", "", "", "")
        all_tests_setup(test_ta, 10, "test", "pW4)", "noCred8@test.com", "3821 N. Oakland Ave, Shorewood, WI 53211",
                        "(414)555-0007")
        failure_msg = "TA account created despite bad name given"
        result_pkg = self.testAdmin.create_user(test_ta)
        self.assertFalse(result_pkg['result'], failure_msg)

    def tearDown(self):
        User.objects.exclude(user_id=1).delete()


class CreateDuplicateAccounts(TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testAdmin = UserAdmin(-1, "", "", "", "", "")
        all_tests_setup(self.testAdmin, 1, "testAdmin", "tA1!", "testAdmin@test.com",
                        "101 W. Wisconsin Ave, Milwaukee, WI 53203", "(414)222-2571")
        # Save to database
        self.an_admin = User()
        setup_database(self.testAdmin, self.an_admin)

    def test_CreateExactDuplicate(self):
        failure_msg = "Somehow created a duplicate account"
        result_pkg = self.testAdmin.create_user(self.testAdmin)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_AccountWithDuplicateID(self):
        new_admin = UserAdmin(-1, "", "", "", "", "")
        all_tests_setup(new_admin, self.testAdmin.user_id, "testAdmin2", "tA2#", "testAdmin2@test.com",
                        "925 N. MLK Dr, Milwaukee, WI 53203", "(414)555-1001")
        failure_msg = "Created admin account with id already taken"
        result_pkg = self.testAdmin.create_user(new_admin)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_AccountWithDuplicateEmail(self):
        new_admin = UserAdmin(-1, "", "", "", "", "")
        all_tests_setup(new_admin, 2, "testAdmin3", "tA3#", self.testAdmin.email, "925 N. MLK Dr, Milwaukee, WI 53203",
                        "(414)555-1001")
        failure_msg = "Created admin account with email already taken"
        result_pkg = self.testAdmin.create_user(new_admin)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_UniqueEmailAndID(self):
        new_admin = self.testAdmin
        all_tests_setup(new_admin, 3, self.testAdmin.name, self.testAdmin.password, "testAdmin4@test.com",
                        self.testAdmin.home_address, self.testAdmin.phone)
        failure_msg = "Admin account not created despite unique email and id"
        result_pkg = self.testAdmin.create_user(new_admin)
        self.assertTrue(result_pkg['result'], failure_msg)

    def tearDown(self):
        User.objects.exclude(user_id=1).delete()


class AccountsWithMissingFields(TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testAdmin = UserAdmin(-1, "", "", "", "", "")
        all_tests_setup(self.testAdmin, 1, "testAdmin", "tA1!", "testAdmin@test.com",
                        "101 W. Wisconsin Ave, Milwaukee, WI 53203", "(414)222-2571")
        # Save to database
        self.an_admin = User()
        setup_database(self.testAdmin, self.an_admin)

    def test_MissingID(self):
        new_instructor = Instructor(-1, "", "", "", "", "")
        all_tests_setup(new_instructor, None, "testInstructor", "tI5*", "testInstructor@test.com",
                        "2600 N. Humboldt Bd, Milwaukee, WI 53201", "(414)444-7654")
        failure_msg = "Created instructor account despite missing id"
        result_pkg = self.testAdmin.create_user(new_instructor)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_MissingPassword(self):
        new_instructor = Instructor(-1, "", "", "", "", "")
        all_tests_setup(new_instructor, 3, "testInstructor3", "", "testInstructor3@test.com",
                        "2601 N. Humboldt Bd, Milwaukee, WI 53201", "(414)444-7655")
        failure_msg = "Created instructor account despite missing password"
        result_pkg = self.testAdmin.create_user(new_instructor)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_MissingName(self):
        new_instructor = Instructor(-1, "", "", "", "", "")
        all_tests_setup(new_instructor, 4, "", "tI5*", "testInstructor4@test.com",
                        "2602 N. Humboldt Bd, Milwaukee, WI 53201", "(414)444-7656")
        failure_msg = "Created instructor account despite missing name"
        result_pkg = self.testAdmin.create_user(new_instructor)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_MissingEmail(self):
        new_instructor = Instructor(-1, "", "", "", "", "")
        all_tests_setup(new_instructor, 5, "testInstructor5", "tI5*", "", "2603 N. Humboldt Bd, Milwaukee, WI 53201",
                        "(414)444-7657")
        failure_msg = "Created instructor account despite missing email"
        result_pkg = self.testAdmin.create_user(new_instructor)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_MissingAddress(self):
        new_instructor = Instructor(-1, "", "", "", "", "")
        all_tests_setup(new_instructor, 6, "testInstructor6", "tI5*", "testInstructor6@test.com", "", "(414)444-7658")
        failure_msg = "Created instructor account despite missing home address"
        result_pkg = self.testAdmin.create_user(new_instructor)
        self.assertFalse(result_pkg['result'], failure_msg)

    def test_MissingPhoneNumber(self):
        new_instructor = Instructor(-1, "", "", "", "", "")
        all_tests_setup(new_instructor, 7, "testInstructor7", "tI5*", "testInstructor7@test.com",
                        "2604 N. Humboldt Bd, Milwaukee, WI 53201", "")
        failure_msg = "Created instructor account despite missing phone number"
        result_pkg = self.testAdmin.create_user(new_instructor)
        self.assertFalse(result_pkg['result'], failure_msg)

    def tearDown(self):
        User.objects.exclude(user_id=1).delete()