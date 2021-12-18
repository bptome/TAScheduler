# Manage Skills unit tests by: Terence Lee (12/17/2021)
from django.test import TestCase

from TAInformation.Models.account_type import AccountType
from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.Models.validator_methods import *


class ManageSkillsAsAdmin(TestCase):
    def setUp(self):
        self.testAdmin = UserAdmin(-1, "", "", "", "", "")
        self.an_admin = User()
        self.other_user = User(user_id=2, name="otherUser", email="namedlater@test.com", password="p2BNl$",
                               home_address="Address to be edited later", phone="(414)555-9999", role=AccountType.TA.value)
        self.testAdmin.skills = {"HTML", "CSS", "Django", "Python", "C"}
        self.other_user.skills.add("Java", "C#", "C")
        all_tests_setup(self.testAdmin, 1, "testAdmin", "tA1)", "testAdmin@test.com",
                        "101 E. Wisconsin Ave., Milwaukee, WI 53202", "(414)555-0001")
        setup_database(self.testAdmin, self.an_admin)

    def test_add_unique_skill_self(self):
        result_info = self.testAdmin.add_skill(self.an_admin, "JavaScript")
        self.assertEqual(result_info['message'], "Unique skill \"JavaScript\" added to your profile\n",
                         msg="Admin wasn\'t able to add unique skill to self")

    def test_add_unique_skill_other(self):
        result_info = self.testAdmin.add_skill(self.other_user, "JavaScript")
        self.assertEqual(result_info['message'], "Unique skill \"JavaScript\" added to otherUser\n",
                         msg="Admin wasn\'t able to add unique skill to other user")

    def test_add_common_skill_self(self):
        result_info = self.testAdmin.add_skill(self.an_admin, "Java")
        self.assertEqual(result_info['message'], "Common skill \"Java\" added to your profile\n",
                         msg="Admin wasn\'t able to added common skill to self")

    def test_add_common_skill_other(self):
        result_info = self.testAdmin.add_skill(self.other_user, "CSS")
        self.assertEqual(result_info['message'], "Common skill \"CSS\" added to otherUser\n",
                         msg="Admin wasn\'t able to add common skill to other user")

    def test_add_blank_skill_self(self):
        result_info = self.testAdmin.add_skill(self.an_admin, "")
        self.assertEqual(result_info['message'], "Can\'t add skill with no name\n",
                         msg="Admin somehow added blank skill to their profile")

    def test_add_whitespace_skill_self(self):
        result_info = self.testAdmin.add_skill(self.an_admin, "  ")
        self.assertEqual(result_info['message'], "Can\'t add skill with no name\n",
                         msg="Admin somehow added no name skill to their profile")

    def test_add_blank_skill_other(self):
        result_info = self.testAdmin.add_skill(self.other_user, "")
        self.assertEqual(result_info['message'], "Can\'t add skill with no name\n",
                         msg="Admin somehow added blank skill to other user")

    def test_add_whitespace_skill_other(self):
        result_info = self.testAdmin.add_skill(self.other_user, "  ")
        self.assertEqual(result_info['message'], "Can\'t add skill with no name\n",
                         msg="Admin somehow added whitespace skill to other user")

    def test_skills_list_self(self):
        result_info = self.testAdmin.list_skills(self.an_admin)
        self.assertEqual(result_info['skills'], {"HTML", "CSS", "Django", "Python"},
                         msg="Admin skills list doesn't match what should be there")

    def test_skills_list_other(self):
        result_info = self.testAdmin.list_skills(self.other_user)
        self.assertEqual(result_info['skills'], {"Java", "C#", "C"},
                         msg="Other user\'s skills list doesn't match what should be there")

    def test_remove_unique_skill_self(self):
        result_info = self.testAdmin.remove_skill(self.an_admin, "Python")
        self.assertEqual(result_info['message'], "Unique skill \"Python\" removed from your profile\n",
                         msg="Admin wasn\'t able to remove unique skill from their profile")

    def test_remove_unique_skill_other(self):
        result_info = self.testAdmin.remove_skill(self.other_user, "C#")
        self.assertEqual(result_info['message'], "Unique skill \"C#\" has been removed from otherUser\n",
                         msg="Admin wasn\'t able to remove unique skill from another user")

    def test_remove_common_skill_self(self):
        result_info = self.testAdmin.remove_skill(self.an_admin, "C")
        self.assertEqual(result_info['message'], "Common skill \"C\" was removed from your profile\n",
                         msg="Admin wasn\'t able to remove common skill from their profile")

    def test_remove_common_skill_other(self):
        result_info = self.testAdmin.remove_skill(self.other_user, "C")
        self.assertEqual(result_info['message'], "Common skill \"C\" was removed from otherUser\n",
                         msg="Admin wasn\'t able to remove common skill from another user")

    def test_remove_blank_skill_self(self):
        result_info = self.testAdmin.remove_skill(self.an_admin, "")
        self.assertEqual(result_info['message'], "Can\'t remove skill without a name\n",
                         msg="Validation on blank skill failed")

    def test_remove_blank_skill_other(self):
        result_info = self.testAdmin.remove_skill(self.other_user, "")
        self.assertEqual(result_info['message'], "Can\'t remove skill without a name\n",
                         msg="Validation on blank skill failed")

    def test_remove_whitespace_skill_self(self):
        result_info = self.testAdmin.remove_skill(self.an_admin, "  ")
        self.assertEqual(result_info['message'], "Can\'t remove skill without a name\n",
                         msg="Validation on just whitespace skill failed")

    def test_remove_whitespace_skill_other(self):
        result_info = self.testAdmin.remove_skill(self.other_user, "  ")
        self.assertEqual(result_info['message'], "Can\'t remove skill without a name\n",
                         msg="Validation on just whitespace skill failed")

    def test_skills_list_id_update(self):
        result_info = self.testAdmin.list_skills(self.an_admin)
        skills_list1 = result_info['skills']
        self.testAdmin.user_id = 3
        result_info = self.testAdmin.list_skills(self.an_admin)
        skills_list2 = result_info['skills']
        self.assertEqual(skills_list1, skills_list2, msg="User id in query did not update with id change")


class ManageSkillsAsInstructor(TestCase):
    def setUp(self):
        self.testInstructor = Instructor(-1, "", "", "", "", "")
        self.an_instructor = User()
        self.other_user = User(user_id=2, name="otherUser", email="namedlater@test.com", password="p2BNl$",
                               home_address="Address to be edited later", phone="(414)555-9999", role=AccountType.TA.value)
        self.testInstructor.skills = {"HTML", "CSS", "Django", "Python", "C"}
        self.other_user.skills.add("Java", "C#", "C")
        all_tests_setup(self.testInstructor, 1, "testInstructor", "tA1)", "testInstructor@test.com",
                        "101 E. Wisconsin Ave., Milwaukee, WI 53202", "(414)555-0001")
        setup_database(self.testInstructor, self.an_instructor)

    def test_add_unique_skill_self(self):
        result_info = self.testInstructor.add_skill(self.an_instructor, "JavaScript")
        self.assertEqual(result_info['message'], "Unique skill \"JavaScript\" added to your profile\n",
                         msg="Instructor wasn\'t able to add unique skill to self")

    def test_add_unique_skill_other(self):
        result_info = self.testInstructor.add_skill(self.other_user, "JavaScript")
        self.assertEqual(result_info['message'], "Instructors can\'t add skill to otherUser\n",
                         msg="Instructor was able to add unique skill to other user")

    def test_add_common_skill_self(self):
        result_info = self.testInstructor.add_skill(self.an_instructor, "Java")
        self.assertEqual(result_info['message'], "Common skill \"Java\" added to your profile\n",
                         msg="Instructor wasn\'t able to added common skill to self")

    def test_add_common_skill_other(self):
        result_info = self.testInstructor.add_skill(self.other_user, "CSS")
        self.assertEqual(result_info['message'], "Instructors can\'t add skill to otherUser\n",
                         msg="Instructor was able to add common skill to other user")

    def test_add_blank_skill_self(self):
        result_info = self.testInstructor.add_skill(self.an_instructor, "")
        self.assertEqual(result_info['message'], "Can\'t add skill with no name\n",
                         msg="Instructor somehow added blank skill to their profile")

    def test_add_whitespace_skill_self(self):
        result_info = self.testInstructor.add_skill(self.an_instructor, "  ")
        self.assertEqual(result_info['message'], "Can\'t add skill with no name\n",
                         msg="Instructor somehow added no name skill to their profile")

    def test_add_blank_skill_other(self):
        result_info = self.testInstructor.add_skill(self.other_user, "")
        self.assertEqual(result_info['message'], "Instructors can\'t add skill to otherUser\n",
                         msg="Validation for skills somehow failed")

    def test_add_whitespace_skill_other(self):
        result_info = self.testInstructor.add_skill(self.other_user, "  ")
        self.assertEqual(result_info['message'], "Instructors can\'t add skill to otherUser\n",
                         msg="Instructor wasn\'t stopped from adding skills to other users")

    def test_skills_list_self(self):
        result_info = self.testInstructor.list_skills(self.an_instructor)
        self.assertEqual(result_info['skills'], {"HTML", "CSS", "Django", "Python"},
                         msg="Instructor skills list doesn't match what should be there")

    def test_skills_list_other(self):
        result_info = self.testInstructor.list_skills(self.other_user)
        self.assertEqual(result_info['message'], "Instructors can\'t view other users' skills\n",
                         msg="Other user\'s skills list is being shown to non-admin account")

    def test_remove_unique_skill_self(self):
        result_info = self.testInstructor.remove_skill(self.an_instructor, "Python")
        self.assertEqual(result_info['message'], "Unique skill \"Python\" was removed from your profile\n",
                         msg="Instructor wasn\'t able to remove unique skill from their profile")

    def test_remove_unique_skill_other(self):
        result_info = self.testInstructor.remove_skill(self.other_user, "C#")
        self.assertEqual(result_info['message'], "Instructors can\'t remove other user\'s skills\n",
                         msg="Instructor wasn able to remove unique skill from another user")

    def test_remove_common_skill_self(self):
        result_info = self.testInstructor.remove_skill(self.an_instructor, "C")
        self.assertEqual(result_info['message'], "Common skill \"C\" was removed from your profile\n",
                         msg="Instructor wasn\'t able to remove common skill from their profile")

    def test_remove_common_skill_other(self):
        result_info = self.testInstructor.remove_skill(self.other_user, "C")
        self.assertEqual(result_info['message'], "Instructors can\'t remove skills from other users\n",
                         msg="Instructor was able to remove common skill from another user")

    def test_remove_blank_skill_self(self):
        result_info = self.testInstructor.remove_skill(self.an_instructor, "")
        self.assertEqual(result_info['message'], "Can\'t remove skill without a name\n",
                         msg="Validation on blank skill failed")

    def test_remove_blank_skill_other(self):
        result_info = self.testInstructor.remove_skill(self.other_user, "")
        self.assertEqual(result_info['message'], "Instructors can\'t remove skills from other users\n",
                         msg="Validation on user permissions failed")

    def test_remove_whitespace_skill_self(self):
        result_info = self.testInstructor.remove_skill(self.an_instructor, "  ")
        self.assertEqual(result_info['message'], "Can\'t remove skill without a name\n",
                         msg="Validation on just whitespace skill failed")

    def test_remove_whitespace_skill_other(self):
        result_info = self.testInstructor.remove_skill(self.other_user, "  ")
        self.assertEqual(result_info['message'], "Instructors can\'t remove skills from other users\n",
                         msg="Validation on user permissions failed")

    def test_skills_list_id_update(self):
        skills_list1 = self.testInstructor.skills
        self.testInstructor.user_id = 3
        skills_list2 = self.testInstructor.skills
        self.assertEqual(skills_list1, skills_list2, msg="User id in query did not update with id change")


class ManageSkillsAsTA(TestCase):
    def setUp(self):
        self.testTA = TA(-1, "", "", "", "", "")
        self.a_ta = User()
        self.other_user = User(user_id=2, name="otherUser", email="namedlater@test.com", password="p2BNl$",
                               home_address="Address to be edited later", phone="(414)555-9999",
                               role=AccountType.TA.value)
        self.testTA.skills = {"HTML", "CSS", "Django", "Python", "C"}
        self.other_user.skills.add("Java", "C#", "C")
        all_tests_setup(self.testTA, 1, "testTA", "tA1)", "testTA@test.com",
                        "101 E. Wisconsin Ave., Milwaukee, WI 53202", "(414)555-0001")
        setup_database(self.testTA, self.a_ta)

    def test_add_unique_skill_self(self):
        result_info = self.testTA.add_skill(self.a_ta, "JavaScript")
        self.assertEqual(result_info['message'], "Unique skill \"JavaScript\" added to your profile\n",
                         msg="TA wasn\'t able to add unique skill to self")

    def test_add_unique_skill_other(self):
        result_info = self.testTA.add_skill(self.other_user, "JavaScript")
        self.assertEqual(result_info['message'], "TAs can\'t add skill to otherUser\n",
                         msg="TA was able to add unique skill to other user")

    def test_add_common_skill_self(self):
        result_info = self.testTA.add_skill(self.a_ta, "Java")
        self.assertEqual(result_info['message'], "Common skill \"Java\" added to your profile\n",
                         msg="TA wasn\'t able to added common skill to self")

    def test_add_common_skill_other(self):
        result_info = self.testTA.add_skill(self.other_user, "CSS")
        self.assertEqual(result_info['message'], "TAs can\'t add skill to otherUser\n",
                         msg="TA was able to add common skill to other user")

    def test_add_blank_skill_self(self):
        result_info = self.testTA.add_skill(self.a_ta, "")
        self.assertEqual(result_info['message'], "Can\'t add skill with no name\n",
                         msg="TA somehow added blank skill to their profile")

    def test_add_whitespace_skill_self(self):
        result_info = self.testTA.add_skill(self.a_ta, "  ")
        self.assertEqual(result_info['message'], "Can\'t add skill with no name\n",
                         msg="TA somehow added no name skill to their profile")

    def test_add_blank_skill_other(self):
        result_info = self.testTA.add_skill(self.other_user, "")
        self.assertEqual(result_info['message'], "TAs can\'t add skill to otherUser\n",
                         msg="Validation for skills somehow failed")

    def test_add_whitespace_skill_other(self):
        result_info = self.testTA.add_skill(self.other_user, "  ")
        self.assertEqual(result_info['message'], "TAs can\'t add skill to otherUser\n",
                         msg="TA wasn\'t stopped from adding skills to other users")

    def test_skills_list_self(self):
        result_info = self.testTA.list_skills(self.a_ta)
        self.assertEqual(result_info['skills'], {"HTML", "CSS", "Django", "Python"},
                         msg="TA skills list doesn't match what should be there")

    def test_skills_list_other(self):
        result_info = self.testTA.list_skills(self.other_user)
        self.assertEqual(result_info['message'], "TAs can\'t view other users' skills\n",
                         msg="Other user\'s skills list is being shown to non-admin account")

    def test_remove_unique_skill_self(self):
        result_info = self.testTA.remove_skill(self.a_ta, "Python")
        self.assertEqual(result_info['message'], "Unique skill \"Python\" was removed from your profile\n",
                         msg="TA wasn\'t able to remove unique skill from their profile")

    def test_remove_unique_skill_other(self):
        result_info = self.testTA.remove_skill(self.other_user, "C#")
        self.assertEqual(result_info['message'], "TAs can\'t remove other user\'s skills\n",
                         msg="TA wasn able to remove unique skill from another user")

    def test_remove_common_skill_self(self):
        result_info = self.testTA.remove_skill(self.a_ta, "C")
        self.assertEqual(result_info['message'], "Common skill \"C\" was removed from your profile\n",
                         msg="TA wasn\'t able to remove common skill from their profile")

    def test_remove_common_skill_other(self):
        result_info = self.testTA.remove_skill(self.other_user, "C")
        self.assertEqual(result_info['message'], "TAs can\'t remove skills from other users\n",
                         msg="TA was able to remove common skill from another user")

    def test_remove_blank_skill_self(self):
        result_info = self.testTA.remove_skill(self.a_ta, "")
        self.assertEqual(result_info['message'], "Can\'t remove skill without a name\n",
                         msg="Validation on blank skill failed")

    def test_remove_blank_skill_other(self):
        result_info = self.testTA.remove_skill(self.other_user, "")
        self.assertEqual(result_info['message'], "TAs can\'t remove skills from other users\n",
                         msg="Validation on user permissions failed")

    def test_remove_whitespace_skill_self(self):
        result_info = self.testTA.remove_skill(self.a_ta, "  ")
        self.assertEqual(result_info['message'], "Can\'t remove skill without a name\n",
                         msg="Validation on just whitespace skill failed")

    def test_remove_whitespace_skill_other(self):
        result_info = self.testTA.remove_skill(self.other_user, "  ")
        self.assertEqual(result_info['message'], "TAs can\'t remove skills from other users\n",
                         msg="Validation on user permissions failed")

    def test_skills_list_id_update(self):
        skills_list1 = self.testTA.skills
        self.testTA.user_id = 3
        skills_list2 = self.testTA.skills
        self.assertEqual(skills_list1, skills_list2, msg="User id in query did not update with id change")