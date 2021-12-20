
from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.base_user import BaseUser
from TAInformation.models import User
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from django.test import Client, TestCase
from TAInformation.Models.validator_methods import all_tests_setup, setup_database


class CreateAccountsAsAdmin(TestCase):
    def setUp(self):
        User.objects.all().delete()
        self.testAdmin = UserAdmin(-1, "", "", "", "", "")
        all_tests_setup(self.testAdmin,
                        1, "testAdmin", "tA1!", "testAdmin@test.com", "101 W. Wisconsin Ave, Milwaukee, WI 53203",
                        "(414)222-2571")

        # Save to database
        self.an_admin = User()
        setup_database(self.testAdmin, self.an_admin)
        self.client = Client()
        self.session = self.client.session
        self.session['user_id'] = self.testAdmin.user_id
        self.session['email'] = self.testAdmin.email
        self.session['role'] = self.testAdmin.role.value
        self.session.save()
        self.session.modified = True

    def test_create_admin(self):
        response = self.client.post("/create_user/",
                                    {'user_id': 2,
                                     'name': "newAdmin",
                                     'password': "t1A!",
                                     'email': "newAdmin@test.com",
                                     'address': "101 W. North Dr., Lake, WI 53200",
                                     'phone': "(414)555-0001",
                                     'role': 3})
        failure_msg = "Couldn\'t create admin account despite having no conflicts"
        self.assertEqual(response.context['message'], "New ADMIN has been created", failure_msg)

    def test_create_instructor(self):
        response = self.client.post("/create_user/",
                                    {'user_id': 2,
                                     'name': "newInstructor",
                                     'password': "tI3+",
                                     'email': "newInstructor@test.com",
                                     'address': "101 W. North Dr., Lake, WI 53200",
                                     'phone': "(414)555-0002",
                                     'role': 2})
        failure_msg = "Couldn\'t create instructor account despite having no conflicts"
        self.assertEqual(response.context['message'], "New INSTRUCTOR has been created", failure_msg)

    def test_create_ta(self):
        response = self.client.post("/create_user/",
                                    {'user_id': 2,
                                     'name': "newTA",
                                     'password': "tI2)",
                                     'email': "newTA@test.com",
                                     'address': "101 W. North Dr., Lake, WI 53200",
                                     'phone': "(414)555-0003",
                                     'role': 1})
        failure_msg = "Couldn\'t create TA account despite having no conflicts"
        self.assertEqual(response.context['message'], "New TA has been created", failure_msg)

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
        self.client = Client()
        self.session = self.client.session
        self.session['user_id'] = self.testInstructor.user_id
        self.session['email'] = self.testInstructor.email
        self.session['role'] = self.testInstructor.role.value
        self.session.save()
        self.session.modified = True

    def test_create_admin(self):
        response = self.client.post("/create_user/",
                                    {'user_id': 2,
                                     'name': "newAdmin",
                                     'password': "t1A!",
                                     'email': "newAdmin@test.com",
                                     'address': "101 W. North Dr., Lake, WI 53200",
                                     'phone': "(414)555-0001",
                                     'role': 3})
        failure_msg = "Created admin account despite not being an admin"
        self.assertEqual(response.context['message'], "Only admins can create new users\n", failure_msg)

    def test_create_instructor(self):
        response = self.client.post("/create_user/",
                                    {'user_id': 2,
                                     'name': "newInstructor",
                                     'password': "tI3+",
                                     'email': "newInstructor@test.com",
                                     'address': "101 W. North Dr., Lake, WI 53200",
                                     'phone': "(414)555-0002",
                                     'role': 2})
        failure_msg = "Created instructor account despite not being an admin"
        self.assertEqual(response.context['message'], "Only admins can create new users\n", failure_msg)

    def test_create_ta(self):
        response = self.client.post("/create_user/",
                                    {'user_id': 2,
                                     'name': "newTA",
                                     'password': "tI2)",
                                     'email': "newTA@test.com",
                                     'address': "101 W. North Dr., Lake, WI 53200",
                                     'phone': "(414)555-0003",
                                     'role': 1})
        failure_msg = "Created TA account despite not being an admin"
        self.assertEqual(response.context['message'], "Only admins can create new users\n", failure_msg)

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
        self.client = Client()
        self.session = self.client.session
        self.session['user_id'] = self.testTA.user_id
        self.session['email'] = self.testTA.email
        self.session['role'] = self.testTA.role.value
        self.session.save()
        self.session.modified = True

    def test_create_admin(self):
        response = self.client.post("/create_user/",
                                    {'user_id': 2,
                                     'name': "newAdmin",
                                     'password': "t1A!",
                                     'email': "newAdmin@test.com",
                                     'address': "101 W. North Dr., Lake, WI 53200",
                                     'phone': "(414)555-0001",
                                     'role': 3})
        failure_msg = "Created admin account despite not being an admin"
        self.assertEqual(response.context['message'], "Only admins can create new users\n", failure_msg)

    def test_create_instructor(self):
        response = self.client.post("/create_user/",
                                    {'user_id': 2,
                                     'name': "newInstructor",
                                     'password': "tI3+",
                                     'email': "newInstructor@test.com",
                                     'address': "101 W. North Dr., Lake, WI 53200",
                                     'phone': "(414)555-0002",
                                     'role': 2})
        failure_msg = "Created instructor account despite not being an admin"
        self.assertEqual(response.context['message'], "Only admins can create new users\n", failure_msg)

    def test_create_ta(self):
        response = self.client.post("/create_user/",
                                    {'user_id': 2,
                                     'name': "newTA",
                                     'password': "tI2)",
                                     'email': "newTA@test.com",
                                     'address': "101 W. North Dr., Lake, WI 53200",
                                     'phone': "(414)555-0003",
                                     'role': 1})
        failure_msg = "Created TA account despite not being an admin"
        self.assertEqual(response.context['message'], "Only admins can create new users\n", failure_msg)

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
        self.client = Client()
        self.session = self.client.session
        self.session['user_id'] = self.testAdmin.user_id
        self.session['email'] = self.testAdmin.email
        self.session['role'] = self.testAdmin.role.value
        self.session.save()
        self.session.modified = True

    def test_NoCredentialsGiven(self):
        response = self.client.post("/create_user/", {
                                     'user_id': 2,
                                     'name': "",
                                     'password': "",
                                     'email': "",
                                     'address': "",
                                     'phone': "",
                                     'role': 1})
        failure_msg = "TA account created despite no credentials given"
        self.assertFalse(response.context['result'], failure_msg)

    def test_NoNameBadPassword(self):
        response = self.client.post("/create_user/", {
            'user_id': 3,
            'name': "",
            'password': "password",
            'email': "noCred2@test.com",
            'address': "3815 N. Oakland Ave, Shorewood, WI 53211",
            'phone': "(414)555-0001",
            'role': 1})
        failure_msg = "TA account created with no name and bad password"
        self.assertFalse(response.context['result'], failure_msg)

    def test_NoNameGoodPassword(self):
        response = self.client.post("/create_user/", {
            'user_id': 4,
            'name': "",
            'password': "aB3$",
            'email': "noCred3@test.com",
            'address': "3816 N. Oakland Ave, Shorewood, WI 53211",
            'phone': "(414)555-0002",
            'role': 1})
        failure_msg = "TA account created despite no name given"
        self.assertFalse(response.context['result'], failure_msg)

    def test_GoodNameNoPassword(self):
        response = self.client.post("/create_user/", {
            'user_id': 5,
            'name': "testTA",
            'password': "",
            'email': "noCred4@test.com",
            'address': "3817 N. Oakland Ave, Shorewood, WI 53211",
            'phone': "(414)555-0003",
            'role': 1})
        failure_msg = "TA account created despite no password given"
        self.assertFalse(response.context['result'], failure_msg)

    def test_GoodNameBadPassword(self):
        response = self.client.post("/create_user/", {
            'user_id': 6,
            'name': "testTA",
            'password': "password",
            'email': "noCred5@test.com",
            'address': "3818 N. Oakland Ave, Shorewood, WI 53211",
            'phone': "(414)555-0004",
            'role': 1})
        failure_msg = "TA account created despite bad password given"
        self.assertFalse(response.context['result'], failure_msg)

    def test_GoodNameGoodPassword(self):
        response = self.client.post("/create_user/", {
            'user_id': 7,
            'name': "testTA",
            'password': "tA1!",
            'email': "goodCreds@test.com",
            'address': "3818 N. Oakland Ave, Shorewood, WI 53211",
            'phone': "(414)555-0005",
            'role': 1})
        failure_msg = "TA account not created despite good credentials given"
        self.assertTrue(response.context['result'], failure_msg)

    def test_BadNameNoPassword(self):
        response = self.client.post("/create_user/", {
            'user_id': 8,
            'name': "test",
            'password': "",
            'email': "noCred6@test.com",
            'address': "3819 N. Oakland Ave, Shorewood, WI 53211",
            'phone': "(414)555-0005",
            'role': 1})
        failure_msg = "TA account created despite bad name and no password given"
        self.assertFalse(response.context['result'], failure_msg)

    def test_BadNameBadPassword(self):
        response = self.client.post("/create_user/", {
            'user_id': 9,
            'name': "test",
            'password': "password",
            'email': "noCred7@test.com",
            'address': "3820 N. Oakland Ave, Shorewood, WI 53211",
            'phone': "(414)555-0006",
            'role': 1})
        failure_msg = "TA account created despite bad credentials given"
        self.assertFalse(response.context['result'], failure_msg)

    def test_BadNameGoodPassword(self):
        response = self.client.post("/create_user/", {
            'user_id': 10,
            'name': "test",
            'password': "pW4)",
            'email': "noCred8@test.com",
            'address': "3821 N. Oakland Ave, Shorewood, WI 53211",
            'phone': "(414)555-0007",
            'role': 1})
        failure_msg = "TA account created despite bad name given"
        self.assertFalse(response.context['result'], failure_msg)

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
        self.client = Client()
        self.session = self.client.session
        self.session['user_id'] = self.testAdmin.user_id
        self.session['email'] = self.testAdmin.email
        self.session['role'] = self.testAdmin.role.value
        self.session.save()
        self.session.modified = True

    def test_CreateExactDuplicate(self):
        response = self.client.post("/create_user/", {
            'user_id': self.testAdmin.user_id,
            'name': self.testAdmin.name,
            'password': self.testAdmin.password,
            'email': self.testAdmin.email,
            'address': self.testAdmin.home_address,
            'phone': self.testAdmin.phone,
            'role': self.testAdmin.role.value
        })
        failure_msg = "Somehow created a duplicate account"
        self.assertEqual(response.context['message'], "User already exists", failure_msg)

    def test_AccountWithDuplicateID(self):
        response = self.client.post("/create_user/", {
            'user_id': self.testAdmin.user_id,
            'name': "testAdmin2",
            'password': "tA2#",
            'email': "testAdmin2@test.com",
            'address': "925 N. MLK Dr, Milwaukee, WI 53203",
            'phone': "(414)555-1001",
            'role': self.testAdmin.role.value
        })
        failure_msg = "Created admin account with id already taken"
        self.assertEqual(response.context['message'], "User already exists", failure_msg)

    def test_AccountWithDuplicateEmail(self):
        response = self.client.post("/create_user/", {
            'user_id': 2,
            'name': "testAdmin3",
            'password': "tA3#",
            'email': self.testAdmin.email,
            'address': "925 N. MLK Dr, Milwaukee, WI 53203",
            'phone': "(414)555-1001",
            'role': self.testAdmin.role.value
        })
        failure_msg = "Created admin account with email already taken"
        self.assertEqual(response.context['message'], "User already exists", failure_msg)

    def test_UniqueEmailAndID(self):
        response = self.client.post("/create_user/", {
            'user_id': 3,
            'name': self.testAdmin.name,
            'password': self.testAdmin.password,
            'email': "testAdmin4@test.com",
            'address': self.testAdmin.home_address,
            'phone': self.testAdmin.phone,
            'role': self.testAdmin.role.value
        })
        failure_msg = "Admin account not created despite unique email and id"
        expected_msg = "New " + self.testAdmin.role.name + " has been created"
        self.assertEqual(response.context['message'], expected_msg, failure_msg)

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
        self.client = Client()
        self.session = self.client.session
        self.session['user_id'] = self.testAdmin.user_id
        self.session['email'] = self.testAdmin.email
        self.session['role'] = self.testAdmin.role.value
        self.session.save()
        self.session.modified = True

    def test_MissingID(self):
        response = self.client.post("/create_user/", {
            'user_id': "",
            'name': "testInstructor",
            'password': "tI5*",
            'email': "testInstructor@test.com",
            'address': "2600 N. Humboldt Bd, Milwaukee, WI 53201",
            'phone': "(414)444-7654",
            'role': 2
        })
        failure_msg = "Created instructor account despite missing id"
        self.assertEqual(response.context['message'], "Invalid user id entered\n", failure_msg)

    def test_MissingPassword(self):
        response = self.client.post("/create_user/", {
            'user_id': 3,
            'name': "testInstructor3",
            'password': "",
            'email': "testInstructor3@test.com",
            'address': "2601 N. Humboldt Bd, Milwaukee, WI 53201",
            'phone': "(414)444-7655",
            'role': 2
        })
        failure_msg = "Created instructor account despite missing password"
        self.assertEqual(response.context['message'], "Password must be at least 4 characters long\n", failure_msg)

    def test_MissingName(self):
        response = self.client.post("/create_user/", {
            'user_id': 4,
            'name': "",
            'password': "tI5*",
            'email': "testInstructor4@test.com",
            'address': "2602 N. Humboldt Bd, Milwaukee, WI 53201",
            'phone': "(414)444-7656",
            'role': 2
        })
        failure_msg = "Created instructor account despite missing name"
        self.assertEqual(response.context['message'], "Invalid name given\n", failure_msg)

    def test_MissingEmail(self):
        response = self.client.post("/create_user/", {
            'user_id': 5,
            'name': "testInstructor5",
            'password': "tI5*",
            'email': "",
            'address': "2603 N. Humboldt Bd, Milwaukee, WI 53201",
            'phone': "(414)444-7657",
            'role': 2
        })
        failure_msg = "Created instructor account despite missing email"
        self.assertNotEqual(response.context['message'], "", failure_msg)

    def test_MissingAddress(self):
        response = self.client.post("/create_user/", {
            'user_id': 6,
            'name': "testInstructor6",
            'password': "tI5*",
            'email': "testInstructor6@test.com",
            'address': "",
            'phone': "(414)444-7658",
            'role': 2
        })
        failure_msg = "Created instructor account despite missing home address"
        self.assertEqual(response.context['message'], "Home address is missing\n", failure_msg)

    def test_MissingPhoneNumber(self):
        response = self.client.post("/create_user/", {
            'user_id': 7,
            'name': "testInstructor7",
            'password': "tI5*",
            'email': "testInstructo7r@test.com",
            'address': "2604 N. Humboldt Bd, Milwaukee, WI 53201",
            'phone': "",
            'role': 2
        })
        failure_msg = "Created instructor account despite missing phone number"
        self.assertEqual(response.context['message'], "No phone number given\n", failure_msg)

    def tearDown(self):
        User.objects.exclude(user_id=1).delete()
