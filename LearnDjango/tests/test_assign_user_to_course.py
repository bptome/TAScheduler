from django.test import TestCase

from LearnDjango.tests.TestAdminDataAccess import add_admin
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.models import Course, User, CourseTAJunction, Lab


class TestAdminAssignTAToCourse(TestCase):
    def setUp(self):
        User(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", 2, "(414)173-4567").save()
        self.test_admin = add_admin()
        self.course1 = Course(1, "CS337", 97, "W 5:00-6:00", "Spring", "Graduate", "hard")
        self.course1.save()
        self.user_ta = User(90, "Omar", "", "", "", 1, "")
        self.user_ta.save()

    def test_valid(self):
        self.test_admin.assign_ta_to_course(self.user_ta, self.course1)
        failure_msg = "TA should be assigned to the course"
        self.assertEqual(CourseTAJunction.objects.get(course_id=self.course1).user_id, self.user_ta, msg=failure_msg)

    def test_valid_two_ta(self):
        user_ta_2 = User(912, "V", "", "", "", 1, "")
        user_ta_2.save()
        self.test_admin.assign_ta_to_course(self.user_ta, self.course1)
        self.test_admin.assign_ta_to_course(user_ta_2, self.course1)
        failure_msg = "2 TAs should be assigned to the Course"
        tas = []
        for j in CourseTAJunction.objects.filter(course_id=self.course1):
            tas.append(j.user_id)
        self.assertEqual(tas, [self.user_ta, user_ta_2], msg=failure_msg)

    def test_attempt_add_admin(self):
        new_admin = User(800, "some admin", "", "", "", 3, "")
        new_admin.save()
        message = self.test_admin.assign_ta_to_course(new_admin, self.course1)
        failure_msg = "Should not be able to add an admin to a lab"
        self.assertEqual(message, "Only TA can be added to a course", msg=failure_msg)

    def test_attempt_add_instructor(self):
        user_instr = User(952, "Terrance", "", "", "", 2, "")
        user_instr.save()
        message = self.test_admin.assign_ta_to_course(user_instr, self.course1)
        failure_msg = "Should not be able to add an instructor to a course"
        self.assertEqual(message, "Only TA can be added to a course", msg=failure_msg)

    def test_TA_already_added(self):
        self.test_admin.assign_ta_to_course(self.user_ta, self.course1)
        failure_msg = "Should not be able to add the same TA twice to the same course"
        self.assertEqual(self.test_admin.assign_ta_to_course(self.user_ta, self.course1), "TA already in this course",
                         msg=failure_msg)


class TestTAOrInstructorAssignToLab(TestCase):
    def setUp(self):
        self.test_instr = Instructor(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", "(414)173-4567")
        User(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", 2, "(414)173-4567").save()
        self.course1 = Course(1, "CS337", 97, "W 5:00-6:00", "Spring", "Graduate", "hard")
        self.course1.save()
        self.error_message = "You must be an Admin to add TA to a course"
        self.test_ta = TA(90, "Omar", "", "", "", "")
        User(90, "Omar", "", "", "", 1, "").save()

    def test_instructor_attempt_message(self):
        message = self.test_instr.assign_ta_to_course(self.test_ta.user_id, self.course1.pk)
        failure_msg = "Correct error message not returned"
        self.assertEqual(message, self.error_message, msg=failure_msg)

    def test_TA_attempt_message(self):
        message = self.test_instr.assign_ta_to_course(self.test_ta.user_id, self.course1.pk)
        failure_msg = "Correct error message not returned"
        self.assertEqual(message, self.error_message, msg=failure_msg)

    def test_instructor_attempt_db_changes(self):
        self.test_instr.assign_ta_to_course(self.test_ta.user_id, self.course1.pk)
        failure_msg = "Instructor cannot add a TA to a Lab, but did"
        self.assertEqual(len(CourseTAJunction.objects.all()), 0, msg=failure_msg)

    def test_TA_attempt_db_changes(self):
        self.test_ta.assign_ta_to_course(self.test_ta.user_id, self.course1.pk)
        failure_msg = "TA cannot add a TA to a Lab, but did"
        self.assertEqual(len(CourseTAJunction.objects.all()), 0, msg=failure_msg)
