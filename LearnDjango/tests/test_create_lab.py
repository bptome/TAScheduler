from django.test import TestCase

from LearnDjango.tests.TestAdminDataAccess import add_admin, add_user_to_test_database, get_course_one_lab
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.models import Lab, LabCourseJunction, User, Course


def model_lab_to_test_array(lab):
    return [lab.lab_name, lab.has_grader, lab.description]


class TestAdminCreateLab(TestCase):
    def setUp(self):
        self.test_admin = add_admin()
        add_user_to_test_database(self.test_admin)
        User(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", 2, "(414)173-4567").save()
        self.course1 = Course(1, "CS337", 97, "W 5:00-6:00", "Spring", "Graduate", "hard")
        self.course1.save()

    def test_valid_entry_lab(self):
        self.test_admin.create_lab("My Lab", False, "My lab for course 1", self.course1)
        new_lab = ["My Lab", False, "My lab for course 1"]
        failure_msg = "Lab should be created"
        self.assertEqual(model_lab_to_test_array(Lab.objects.get(lab_id=1)), new_lab, msg=failure_msg)

    def test_valid_one_lab_course(self):
        self.test_admin.create_lab("My Lab", False, "My lab for course 1", self.course1)
        new_lab = ["My Lab", False, "My lab for course 1"]
        labs = []
        for junction in LabCourseJunction.objects.filter(course_id=self.course1):
            labs.append(model_lab_to_test_array(junction.lab_id))
        failure_msg = "Lab should be assigned to the course"
        self.assertEqual(labs, [new_lab], msg=failure_msg)

    def test_valid_two_lab_course(self):
        self.test_admin.create_lab("My Lab", False, "My lab for course 1", self.course1)
        self.test_admin.create_lab("My Lab 2", True, "My second Lab for Course 1", self.course1)
        labs = []
        for junction in LabCourseJunction.objects.filter(course_id=self.course1):
            labs.append(model_lab_to_test_array(junction.lab_id))
        new_lab = ["My Lab", False, "My lab for course 1"]
        new_lab2 = ["My Lab 2", True, "My second Lab for Course 1"]
        failure_msg = "2 labs should be assigned to the course"
        self.assertEqual(labs, [new_lab, new_lab2], msg=failure_msg)

    def test_valid_lab_two_courses_in_system(self):
        get_course_one_lab()
        self.test_admin.create_lab("My Lab", False, "My lab for course 2", self.course1)
        new_lab = ["My Lab", False, "My lab for course 2"]
        labs = []
        for junction in LabCourseJunction.objects.filter(course_id=self.course1):
            labs.append(model_lab_to_test_array(junction.lab_id))
        failure_msg = "Lab should be assigned to the course"
        self.assertEqual(labs, [new_lab], msg=failure_msg)

    def test_taken_lab_id_message(self):
        self.test_admin.create_lab("My Lab", False, "My Lab for Course 2", self.course1)
        message = self.test_admin.create_lab("My Lab", False, "My Lab for Course 2", self.course1)
        failure_msg = "Duplicate lab_id message should be returned"
        self.assertEqual(message, "Lab name already created for this course", msg=failure_msg)

    def test_taken_lab_id_db_changes(self):
        self.test_admin.create_lab("My Lab", False, "My Lab for Course 2", self.course1)
        self.test_admin.create_lab("My Lab", False, "My Lab for Course 2", self.course1)
        failure_msg = "A lab was added incorrectly"
        self.assertEqual(len(Lab.objects.all()), 1, msg=failure_msg)


class TestOtherUserCreateLab(TestCase):
    def setUp(self):
        User(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", 2, "(414)173-4567").save()
        self.course1 = Course(1, "CS337", 97, "W 5:00-6:00", "Spring", "Graduate", "hard")
        self.course1.save()
        self.error_message = "You must be an Admin to add Labs"

    def test_instructor_attempt_message(self):
        test_instructor = Instructor(1, "", "", "", "", "")
        message = test_instructor.create_lab("My Lab", False, "My Lab for Course 2", self.course1)
        failure_msg = "Correct error message not returned"
        self.assertEqual(message, self.error_message, msg=failure_msg)

    def test_TA_attempt_message(self):
        test_TA = TA(1, "", "", "", "", "")
        message = test_TA.create_lab("My Lab", False, "My Lab for Course 2", self.course1)
        failure_msg = "Correct error message not returned"
        self.assertEqual(message, self.error_message, msg=failure_msg)

    def test_instructor_attempt_db_changes(self):
        test_instructor = Instructor(1, "", "", "", "", "")
        test_instructor.create_lab("My Lab", False, "My Lab for Course 2", self.course1)
        failure_msg = "Instructor cannot add to the db, but did"
        self.assertEqual(len(Lab.objects.all()), 0, msg=failure_msg)

    def test_TA_attempt_db_changes(self):
        test_TA = TA(1, "", "", "", "", "")
        test_TA.create_lab("My Lab", False, "My Lab for Course 2", self.course1)
        failure_msg = "TA cannot add to the db, but did"
        self.assertEqual(len(Lab.objects.all()), 0, msg=failure_msg)