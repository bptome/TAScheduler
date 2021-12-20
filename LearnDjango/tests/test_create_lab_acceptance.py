from django.test import TestCase, Client

from LearnDjango.tests.TestAdminDataAccess import add_admin, add_user_to_test_database
from TAInformation.models import User, Course, Lab, LabCourseJunction


class AdminCreateLab(TestCase):
    def setUp(self):
        add_user_to_test_database(add_admin())
        instr = User(4, "Instructor", "password2", "email3@gmail.com", "address3", 2, "563520562")
        instr.save()
        self.course = Course(16, "CS150", instr.pk, "meeting time", "fall", "course type", "description")
        self.course.save()
        self.lab = Lab(16, "Lab", "description")
        self.lab.save()
        LabCourseJunction(5, self.lab.pk, self.course.pk).save()
        self.firstResponse = self.client.post("/", {"email": "testAdmin@test.com", "password": "tA1!"}, follow=True)
        self.length = len(Lab.objects.all())

    def test_valid_entry_ta_in_course_message(self):
        response = self.client.post("/labs/", {"lab": "Newest Lab", "course": self.course.course_name, "description": "Test Description"}, follow=True)
        failure_msg = "Incorrect message for valid entry"
        self.assertEqual(response.context['message'], "Lab saved to course", msg=failure_msg)

    def test_valid_entry_lab_added(self):
        self.client.post("/labs/", {"lab": "Newest Lab", "course": self.course.course_name, "description": "Test Description"}, follow=True)
        failure_msg = "Lab not added to DB"
        self.assertEqual(Lab.objects.get(lab_id=self.lab.pk), self.lab, msg=failure_msg)

    def test_valid_entry_course_lab_junction(self):
        self.client.post("/labs/", {"lab": "Newest Lab", "course": self.course.course_name, "description": "Test Description"}, follow=True)
        failure_msg = "Lab junction not added to DB"
        self.assertEqual(LabCourseJunction.objects.get(lab_id=self.lab).course_id, self.course, msg=failure_msg)

    def test_invalid_course_message(self):
        self.client.post("/labs/", {"lab": "Newest Lab", "course": "bad course", "description": "Test Description"}, follow=True)
        failure_msg = "Incorrect message for no course"
        self.assertEqual(self.length, len(Lab.objects.all()), msg=failure_msg)

    def test_invalid_course_lab_db(self):
        response = self.client.post("/labs/", {"lab": "Newest Lab", "course": "bad course", "description": "Test Description"}, follow=True)
        failure_msg = "Incorrect DB change for no course"
        self.assertEqual(response.context['message'], "Course not found", msg=failure_msg)

    def test_lab_already_added_message(self):
        response = self.client.post("/labs/", {"lab": self.lab.lab_name, "course": self.course.course_name, "description": "Test Description"}, follow=True)
        failure_msg = "Incorrect message for lab already added to course"
        self.assertEqual("Lab name already created for this course", response.context['message'], msg=failure_msg)

    def test_lab_already_added_lab_db(self):
        response = self.client.post("/labs/", {"lab": self.lab.lab_name, "course": self.course.course_name, "description": "Test Description"}, follow=True)
        failure_msg = "Incorrect DB for lab already added to course"
        self.assertEqual(self.length, len(Lab.objects.all()), msg=failure_msg)

    def test_empty_fields(self):
        self.client.post("/labs/", {"lab": "", "course": "",
                                    "description": "Test Description"}, follow=True)
        failure_msg = "added lab despite empty fields"
        self.assertEqual(self.length, len(Lab.objects.all()), msg=failure_msg)
        self.client.post("/labs/", {"lab": self.lab.lab_name, "course": "",
                                    "description": "Test Description"}, follow=True)
        self.assertEqual(self.length, len(Lab.objects.all()), msg=failure_msg)
        self.client.post("/labs/", {"lab": "", "course": self.course.course_name,
                                    "description": ""}, follow=True)
        self.assertEqual(self.length, len(Lab.objects.all()), msg=failure_msg)

    def test_two_courses_same_name(self):
        Course(76, "CS150", 4, "W 5:00-6:00", "Spring", "Graduate", "hard").save()
        response = self.client.post("/labs/", {"lab": "Newest Lab", "course": self.course.course_name, "description": "Test Description"}, follow=True)
        failure_msg = "Message incorrect for double course name"
        self.assertEqual(response.context['message'], "Lab saved to course", msg=failure_msg)

class TestOtherUserCreateLab(TestCase):
    def setUp(self):
        add_user_to_test_database(add_admin())
        ta = User(2, "New TA", "password", "email@gmail.com", "address", 1, "51352056")
        ta.save()
        # User.objects.create(3, "New TA 2", "password2", "email2@gmail.com", "address2", 1, "513520562")
        instr = User(4, "Instructor", "password2", "email3@gmail.com", "address3", 2, "563520562")
        instr.save()
        self.course = Course(16, "CS150", instr.pk, "meeting time", "fall", "course type", "description")
        self.course.save()
        self.lab = Lab(16, "Lab", "description")
        self.lab.save()
        LabCourseJunction(5, self.lab.pk, self.course.pk).save()


    def test_ta_attempt_message(self):
        self.client.post("/", {"email": "email@gmail.com", "password": "password"}, follow=True)
        response = self.client.post("/labs/", {"lab": "Newest Lab", "course": self.course.course_name, "description": "Test Description"}, follow=True)
        failure_msg = "Incorrect message for TA attempt to add a lab"
        self.assertEqual("You must be an Admin to add Labs", response.context['message'], msg=failure_msg)

    def test_TA_attempt_db_changes(self):
        self.client.post("/", {"email": "email@gmail.com", "password": "password"}, follow=True)
        length = len(Lab.objects.all())
        self.client.post("/labs/", {"lab": "Newest Lab", "course": self.course.course_name, "description": "Test Description"}, follow=True)
        failure_msg = "Incorrect DB change for TA attempt to add a lab"
        self.assertEqual(length, len(Lab.objects.all()), msg=failure_msg)

    def test_instructor_attempt_message(self):
        self.client.post("/", {"email": "email3@gmail.com", "password": "password2"}, follow=True)
        response = self.client.post("/labs/", {"lab": "Newest Lab", "course": self.course.course_name,
                                               "description": "Test Description"}, follow=True)
        failure_msg = "Incorrect message for Instructor attempt to add a lab"
        self.assertEqual("You must be an Admin to add Labs", response.context['message'], msg=failure_msg)

    def test_instructor_attempt_db_changes(self):
        self.client.post("/", {"email": "email3@gmail.com", "password": "password2"}, follow=True)
        length = len(Lab.objects.all())
        self.client.post("/labs/", {"lab": "Newest Lab", "course": self.course.course_name, "description": "Test Description"}, follow=True)
        failure_msg = "Incorrect message for Instructor attempt to add a lab"
        self.assertEqual(length, len(Lab.objects.all()), msg=failure_msg)