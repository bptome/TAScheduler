from django.test import TestCase

from LearnDjango.tests.TestAdminDataAccess import add_admin
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.models import Course, User, LabTAJunction, Lab, CourseTAJunction, LabCourseJunction


class TestAdminAssignTAToLab(TestCase):
    def setUp(self):
        User(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", 2, "(414)173-4567").save()
        self.test_admin = add_admin() # instantiates a test_admin object
        self.course1 = Course(1, "CS337", 97, "W 5:00-6:00", "Spring", "Graduate", "hard")
        self.course1.save()
        self.lab1 = Lab(1, "My Lab", False, "My Lab for Course 1")
        self.lab1.save()
        self.user_ta = User(90, "Omar", "", "", "", 1, "")
        self.user_ta.save()
        LabCourseJunction.objects.create(lab_id=self.lab1, course_id=self.course1)

    def test_valid(self):
        self.test_admin.assign_ta_to_lab(self.user_ta, self.lab1)
        failure_msg = "TA should be assigned to the Lab"
        self.assertEqual(LabTAJunction.objects.get(lab_id=self.lab1.pk).user_id, self.user_ta, msg=failure_msg)

    def test_valid_message(self):
        failure_msg = "Incorrect message for valid assignment"
        self.assertEqual(self.test_admin.assign_ta_to_lab(self.user_ta, self.lab1), "TA assigned to lab and course", msg=failure_msg)

    def test_valid_not_in_course(self):
        self.test_admin.assign_ta_to_lab(self.user_ta, self.lab1)
        failure_msg = "TA should be assigned to the Lab"
        self.assertEqual(CourseTAJunction.objects.get(user_id=self.user_ta).course_id, self.course1, msg=failure_msg)

    def test_valid_already_in_course(self):
        CourseTAJunction.objects.create(user_id=self.user_ta, course_id=self.course1)
        self.test_admin.assign_ta_to_lab(self.user_ta, self.lab1)
        failure_msg = "TA should be assigned to the Lab"
        self.assertEqual(len(CourseTAJunction.objects.filter(user_id=self.user_ta)), 1, msg=failure_msg)

    def test_valid_already_in_course_message(self):
        CourseTAJunction.objects.create(user_id=self.user_ta, course_id=self.course1)
        failure_msg = "Incorrect message for TA already in course"
        self.assertEqual(self.test_admin.assign_ta_to_lab(self.user_ta, self.lab1), "TA assigned to lab", msg=failure_msg)

    def test_valid_two_ta(self):
        user_ta_2 = User(912, "V", "", "", "", 1, "")
        user_ta_2.save()
        self.test_admin.assign_ta_to_lab(self.user_ta, self.lab1)
        self.test_admin.assign_ta_to_lab(user_ta_2, self.lab1)
        users = []
        for e in LabTAJunction.objects.filter(lab_id=self.lab1):
            users.append(e.user_id)
        failure_msg = "2 TAs should be assigned to the Lab"
        self.assertEqual(users, [self.user_ta, user_ta_2], msg=failure_msg)

    def test_attempt_add_admin(self):
        user_admin = User(955, "Terrance", "", "", "", 3, "")
        user_admin.save()
        message = self.test_admin.assign_ta_to_lab(user_admin, self.lab1)
        failure_msg = "Should not be able to add an admin to a lab"
        self.assertEqual(message, "Only TA can be added to lab", msg=failure_msg)

    def test_attempt_add_instructor(self):
        user_instr = User(952, "Terrance", "", "", "", 2, "")
        message = self.test_admin.assign_ta_to_lab(user_instr, self.lab1)
        failure_msg = "Should not be able to add an instructor to a lab"
        self.assertEqual(message, "Only TA can be added to lab", msg=failure_msg)

    def test_TA_already_added(self):
        user_ta = User(90, "Omar", "", "", "", 1, "")
        user_ta.save()
        self.test_admin.assign_ta_to_lab(user_ta, self.lab1)
        failure_msg = "Should not be able to add the same TA twice to the same lab"
        self.assertEqual(self.test_admin.assign_ta_to_lab(user_ta, self.lab1), "TA already in lab", msg=failure_msg)


class TestTAOrInstructorAssignToLab(TestCase):
    def setUp(self):
        self.test_instr= Instructor(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", "(414)173-4567")
        User(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", 2, "(414)173-4567").save()
        self.course1 = Course(1, "CS337", 97, "W 5:00-6:00", "Spring", "Graduate", "hard")
        self.course1.save()
        self.lab1 = Lab(1, "My Lab", False, "My Lab for Course 1")
        self.lab1.save()
        self.error_message = "You must be an Admin to add a TA to a Lab"
        self.test_ta = TA(90, "Omar", "", "", "", "")
        User(90, "Omar", "", "", "", 1, "").save()

    def test_instructor_attempt_message(self):
        message = self.test_instr.assign_ta_to_lab(self.test_ta.user_id, self.lab1.pk)
        failure_msg = "Correct error message not returned"
        self.assertEqual(message, self.error_message, msg=failure_msg)

    def test_TA_attempt_message(self):
        message = self.test_instr.assign_ta_to_lab(self.test_ta.user_id, self.lab1.pk)
        failure_msg = "Correct error message not returned"
        self.assertEqual(message, self.error_message, msg=failure_msg)

    def test_instructor_attempt_db_changes(self):
        self.test_instr.assign_ta_to_lab(self.test_ta.user_id, self.lab1.pk)
        failure_msg = "Instructor cannot add a TA to a Lab, but did"
        self.assertEqual(len(LabTAJunction.objects.all()), 0, msg=failure_msg)

    def test_TA_attempt_db_changes(self):
        self.test_ta.assign_ta_to_lab(self.test_ta.user_id, self.lab1.pk)
        failure_msg = "TA cannot add a TA to a Lab, but did"
        self.assertEqual(len(LabTAJunction.objects.all()), 0, msg=failure_msg)