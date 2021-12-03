import unittest
from .models import MyUser


class ValidLogInAsUser(unittest.TestCase):
    def setUp(self):
        self.testUser = myUser()
        self.testUser.email = "testUser@test.com"
        self.testUser.password = "testUser"
        self.testUser.save()

    def test_ValidEmailAndPassword(self):
        failure_msg = "Couldn\'t log in despite having valid credentials"
        self.assertTrue(self.login(testUser.email, testUser.password), failure_msg)

    def test_ValidEmailAndInvalidPassword(self):
        false_password = "fake"
        failure_msg = "Logged in despite having invalid credentials"
        self.assertFalse(self.login(testUser.email, false_password), failure_msg)

    def test_InvalidEmailAndValidPassword(self):
        false_email = "fakeUser@test.com"
        failure_msg = "Logged in despite having invalid credentials"
        self.assertFalse(self.login(false_email, testUser.password), failure_msg)

    def test_InvalidEmailThenValidInput(self):
        false_email = "fakeUser@test.com"
        failure_msg = "Logged in despite having invalid credentials"
        self.assertFalse(self.login(false_email, testUser.password), failure_msg)
        failure_msg = "Couldn\'t log in despite having valid credentials"
        self.assertTrue(self.login(testUser.email, testUser.password), failure_msg)

    def test_EmptyEmailAndPassword(self):
        empty_email = ""
        empty_password = ""
        self.testUser.email = empty_email
        self.testUser.password = empty_password
        self.testUser.save()

        failure_msg = "Logged in despite having no email and password"
        self.assertFalse(self.login(empty_email, empty_password), failure_msg)


class ValidLogInWithRoles(unittest.TestCase):
    def setUp(self):
        self.testUser = myUser()
        self.testUser.email = "testUser@test.com"
        self.testUser.password = "testUser"
        self.testUser.save()

    def test_ValidLogInAsAdmin(self):
        self.testUser.role = AccountType.ADMIN
        self.testUser.save()
        failure_msg = "Couldn\'t log in despite having valid credentials as an admin"
        self.assertTrue(self.login(testUser.email, testUser.password), failure_msg)

    def test_ValidLogInAsTA(self):
        self.testUser.role = AccountType.TA
        self.testUser.save()
        failure_msg = "Couldn\'t log in despite having valid credentials as a TA"
        self.assertTrue(self.login(testUser.email, testUser.password), failure_msg)

    def test_ValidLogInAsInstructor(self):
        self.testUser.role = AccountType.INSTRUCTOR
        self.testUser.save()
        failure_msg = "Couldn\'t log in despite having valid credentials as an instructor"
        self.assertTrue(self.login(testUser.email, testUser.password), failure_msg)

    def test_InvalidLogInAsAdmin(self):
        self.testUser.role = AccountType.ADMIN
        self.testUser.save()

        false_password = "fake"
        failure_msg = "Logged in despite having invalid credentials as an admin"
        self.assertFalse(self.login(testUser.email, false_password), failure_msg)

    def test_InvalidLogInAsTA(self):
        self.testUser.role = AccountType.TA
        self.testUser.save()

        false_password = "fake"
        failure_msg = "Logged in despite having invalid credentials as a TA"
        self.assertFalse(self.login(testUser.email, false_password), failure_msg)

    def test_InvalidLogInAsInstructor(self):
        self.testUser.role = AccountType.INSTRUCTOR
        self.testUser.save()

        false_password = "fake"
        failure_msg = "Logged in despite having invalid credentials as an instructor"
        self.assertFalse(self.login(testUser.email, false_password), failure_msg)


class InvalidEmailLogIn(unittest.TestCase):

    def setUp(self):
        self.testUser = myUser()
        self.testUser.email = "testUser@test.com"
        self.testUser.password = "testUser"
        self.testUser.save()

    def test_TooLongEmailLogIn(self):
        long_email = "VeryLongUserNameOverTwentyCharacters@test.com"
        self.testUser.email = long_email;
        self.testUser.save()

        failure_msg = "Logged in despite having invalid email(too long)"
        self.assertFalse(self.login(long_email, testUser.password), failure_msg)

    def test_TooShortEmailLogIn(self):
        short_email = "@test.com"
        self.testUser.email = short_email;
        self.testUser.save()

        failure_msg = "Logged in despite having invalid email(too short)"
        self.assertFalse(self.login(short_email, testUser.password), failure_msg)

    def test_InvalidEmailFormatLogIn(self):
        invalid_email = "useremailtest.com"
        self.testUser.email = invalid_email;
        self.testUser.save()

        failure_msg = "Logged in despite having invalid email(no @ symbol)"
        self.assertFalse(self.login(invalid_email, testUser.password), failure_msg)

    def test_EmptyEmailLogIn(self):
        empty_email = ""
        self.testUser.email = empty_email
        self.testUser.save()

        failure_msg = "Logged in despite having no email"
        self.assertFalse(self.login(empty_email, empty_password), failure_msg)

    def test_InvalidEmailEndingLogIn(self):
        invalid_email = "fakeuseremail"
        self.testUser.email = invalid_email;
        self.testUser.save()

        failure_msg = "Logged in despite having invalid email format(no @___. ending)"
        self.assertFalse(self.login(invalid_email, testUser.password), failure_msg)


class InvalidPasswordLogIn(unittest.TestCase):

    def setUp(self):
        self.testUser = myUser()
        self.testUser.email = "testUser@test.com"
        self.testUser.password = "testUser"
        self.testUser.save()

    def test_TooLongPasswordLogIn(self):
        long_password = "VeryLongPasswordOverTwentyCharacters"
        self.testUser.password = long_password;
        self.testUser.save()

        failure_msg = "Logged in despite having invalid password(too long)"
        self.assertFalse(self.login(self.testUser.email, long_password), failure_msg)

    def test_TooShortPasswordLogIn(self):
        short_password = "a"
        self.testUser.password = short_password;
        self.testUser.save()

        failure_msg = "Logged in despite having invalid password(too short)"
        self.assertFalse(self.login(self.testUser.email, short_password), failure_msg)

    def test_EmptyPasswordLogIn(self):
        empty_password = ""
        self.testUser.password = empty_password;
        self.testUser.save()

        failure_msg = "Logged in despite having empty password"
        self.assertFalse(self.login(self.testUser.email, empty_password), failure_msg)
