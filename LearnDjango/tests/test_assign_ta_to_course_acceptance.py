from django.test import TestCase, Client

from LearnDjango.tests.TestAdminDataAccess import add_admin, add_user_to_test_database
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.models import User, Course, CourseTAJunction


class TestAdminAssignTAToCourse(TestCase):
    def setUp(self):
        User(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", 2, "(414)173-4567").save()
        self.test_admin = add_admin()
        self.course1 = Course(1, "CS337", 97, "W 5:00-6:00", "Spring", "Graduate", "hard")
        add_user_to_test_database(add_admin())
        self.course1.save()
        self.user_ta = User(90, "Omar", "", "", "", 1, "")
        self.user_ta.save()
        self.firstResponse = self.client.post("/", {"email": "testAdmin@test.com", "password": "tA1!"}, follow=True)
        self.length = len(CourseTAJunction.objects.all())

    def test_valid(self):
        self.client.post("/courses/",
                         {"course": self.course1.course_name, "ta": self.user_ta.name, "addToCourse": "true"})
        failure_msg = "TA should be assigned to the course in the DB"
        self.assertEqual(CourseTAJunction.objects.get(course_id=self.course1).user_id, self.user_ta, msg=failure_msg)

    def test_valid_message(self):
        response = self.client.post("/courses/", {"course": self.course1.course_name, "ta": self.user_ta.name,
                                                  "addToCourse": "true"})
        failure_msg = "TA should be assigned to the course message incorrect"
        self.assertEqual(response.context['message'], "TA assigned to course", msg=failure_msg)

    def test_valid_two_ta(self):
        user_ta_2 = User(912, "V", "", "", "", 1, "")
        user_ta_2.save()
        self.client.post("/courses/",
                         {"course": self.course1.course_name, "ta": self.user_ta.name, "addToCourse": "true"})
        self.client.post("/courses/", {"course": self.course1.course_name, "ta": user_ta_2.name, "addToCourse": "true"})
        failure_msg = "2 TAs should be assigned to the Course"
        tas = []
        for j in CourseTAJunction.objects.filter(course_id=self.course1):
            tas.append(j.user_id)
        self.assertEqual(tas, [self.user_ta, user_ta_2], msg=failure_msg)

    def test_attempt_add_admin_message(self):
        new_admin = User(800, "some admin", "", "", "", 3, "")
        new_admin.save()
        response = self.client.post("/courses/",
                                    {"course": self.course1.course_name, "ta": new_admin.name, "addToCourse": "true"})
        failure_msg = "Incorrect message for not being able to add an admin to a lab"
        self.assertEqual(response.context['message'], "Only TA can be added to a course", msg=failure_msg)

    def test_attempt_add_admin_message(self):
        new_admin = User(800, "some admin", "", "", "", 3, "")
        new_admin.save()
        response = self.client.post("/courses/",
                                    {"course": self.course1.course_name, "ta": new_admin.name, "addToCourse": "true"})
        failure_msg = "Incorrect message for not being able to add an admin to a lab"
        self.assertEqual(response.context['message'], "Only TA can be added to a course", msg=failure_msg)

    def test_attempt_add_instructor_message(self):
        user_instr = User(952, "Terrance", "", "", "", 2, "")
        user_instr.save()
        response = self.client.post("/courses/",
                                    {"course": self.course1.course_name, "ta": user_instr.name, "addToCourse": "true"})
        failure_msg = "Incorrect message for not being able to add an instructor to a course"
        self.assertEqual(response.context['message'], "Only TA can be added to a course", msg=failure_msg)

    def test_TA_already_added_message(self):
        self.client.post("/courses/",
                         {"course": self.course1.course_name, "ta": self.user_ta.name, "addToCourse": "true"})
        response = self.client.post("/courses/",
                                    {"course": self.course1.course_name, "ta": self.user_ta.name,
                                     "addToCourse": "true"})
        failure_msg = "Incorrect message for adding the same TA twice to the same course"
        self.assertEqual(response.context["message"], "TA already in this course", msg=failure_msg)

    def test_empty_fields(self):
        failure_msg = "DB changed desite empty fields"
        self.client.post("/courses/",
                         {"course": "", "ta": "", "addToCourse": "true"})
        self.assertEqual(self.length, len(CourseTAJunction.objects.all()), msg=failure_msg)

        self.client.post("/courses/",
                         {"course": self.course1.course_name, "ta": "", "addToCourse": "true"})
        self.assertEqual(self.length, len(CourseTAJunction.objects.all()), msg=failure_msg)

        self.client.post("/courses/",
                         {"course": "", "ta": self.user_ta.name, "addToCourse": "true"})
        self.assertEqual(self.length, len(CourseTAJunction.objects.all()), msg=failure_msg)

    def test_two_users_same_name(self):
        user_ta_2 = User(91, "Omar", "", "", "", 1, "")
        user_ta_2.save()
        response = self.client.post("/courses/",
                                    {"course": self.course1.course_name, "ta": user_ta_2.name, "addToCourse": "true"})
        failure_msg = "Message incorrect for double TA name"
        self.assertEqual(response.context['message'], "TA assigned to course", msg=failure_msg)

    def test_two_courses_same_name(self):
        Course(76, "CS337", 97, "W 5:00-6:00", "Spring", "Graduate", "hard").save()
        response = self.client.post("/courses/",
                                    {"course": self.course1.course_name, "ta": self.user_ta.name, "addToCourse": "true"})
        failure_msg = "Message incorrect for double course name"
        self.assertEqual(response.context['message'], "TA assigned to course", msg=failure_msg)


class TestTAOrInstructorAssignToLab(TestCase):
    def setUp(self):
        self.test_instr = Instructor(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", "(414)173-4567")
        User(97, "Bob Sorenson", "ter7asdfythg", "bob@uwm.edu", "Kenwoood ave", 2, "(414)173-4567").save()
        self.course1 = Course(1, "CS337", 97, "W 5:00-6:00", "Spring", "Graduate", "hard")
        self.course1.save()
        self.error_message = "You must be an Admin to add TA to a course"
        self.test_ta = TA(90, "Omar", "ter7asdfythg!", "omar@email.com", "", "")
        User(90, "Omar", "ter7asdfythg!", "omar@email.com", "", 1, "").save()
        self.length = len(CourseTAJunction.objects.all())

    def test_instructor_attempt_message(self):
        self.client.post("/", {"email": "bob@uwm.edu", "password": "ter7asdfythg!"}, follow=True)
        response = self.client.post("/courses/", {"course": self.course1.course_name, "ta": self.test_ta.name,
                                                  "addToCourse": "true"})
        failure_msg = "Correct error message not returned for instructor trying to assign TA to a course"
        self.assertEqual(response.context['message'], self.error_message, msg=failure_msg)

    def test_TA_attempt_message(self):
        self.client.post("/", {"email": "omar@email.com", "password": "ter7asdfythg!"}, follow=True)
        response = self.client.post("/courses/", {"course": self.course1.course_name, "ta": self.test_ta.name,
                                                  "addToCourse": "true"})
        failure_msg = "Correct error message not returned for TA trying to assign TA to a course"
        self.assertEqual(response.context['message'], self.error_message, msg=failure_msg)

    def test_instructor_attempt_db_changes(self):
        self.client.post("/", {"email": "bob@uwm.edu", "password": "ter7asdfythg!"}, follow=True)
        self.client.post("/courses/",
                         {"course": self.course1.course_name, "ta": self.test_ta.name, "addToCourse": "true"})
        failure_msg = "Instructor cannot add a TA to a Lab, but did"
        self.assertEqual(self.length, len(CourseTAJunction.objects.all()), msg=failure_msg)

    def test_TA_attempt_db_changes(self):
        self.client.post("/", {"email": "omar@email.com", "password": "ter7asdfythg!"}, follow=True)
        self.client.post("/courses/",
                         {"course": self.course1.course_name, "ta": self.test_ta.name, "addToCourse": "true"})
        failure_msg = "TA cannot add a TA to a Lab, but did"
        self.assertEqual(self.length, len(CourseTAJunction.objects.all()), msg=failure_msg)
