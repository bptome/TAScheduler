from django.test import TestCase

from TAInformation.Models.account_type import AccountType


class TestStr(TestCase):
    def test_admin(self):
        e = AccountType.ADMIN
        self.assertEqual("Admin", e.__str__(), msg="Should return Admin")

    def test_instructor(self):
        e = AccountType.INSTRUCTOR
        self.assertEqual("Instructor", e.__str__(), msg="Should return Instructor")

    def test_TA(self):
        e = AccountType.TA
        self.assertEqual("TA", e.__str__(), msg="Should return TA")

    def test_default(self):
        e = AccountType.DEFAULT
        self.assertEqual("Default", e.__str__(), msg="Should return Default")
