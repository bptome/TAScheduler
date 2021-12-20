from django.test import TestCase, Client

from LearnDjango.tests.TestAdminDataAccess import add_admin, add_user_to_test_database
from TAInformation.models import User, Course, Lab, LabCourseJunction, CourseTAJunction, LabTAJunction


class AdminAssignTAToLab(TestCase):
    def setUp(self):
        add_user_to_test_database(add_admin())
        self.ta = User(56, "New TA Name", "password", "email@gmail.com", "address", 1, "51352056")
        self.ta.save()
        # User.objects.create(3, "New TA 2", "password2", "email2@gmail.com", "address2", 1, "513520562")
        instr = User(4, "Instructor", "password2", "email3@gmail.com", "address3", 2, "563520562")
        instr.save()
        self.course = Course(16, "CS150", instr.pk, "meeting time", "fall", "course type", "description")
        self.course.save()
        self.lab = Lab(16, "Lab", "description")
        self.lab.save()
        LabCourseJunction(5, self.lab.pk, self.course.pk).save()
        self.firstResponse = self.client.post("/", {"email": "testAdmin@test.com", "password": "tA1!"}, follow=True)
        self.length = len(LabTAJunction.objects.all())

    def test_valid_entry_TA_in_course_message(self):
        CourseTAJunction(5, self.course.pk, self.ta.pk).save()
        response = self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Incorrect message for valid entry for ta already in course"
        self.assertEqual(response.context['message'], "TA assigned to lab", msg=failure_msg)

    def test_invalid_entry_TA_in_course_message(self):
        CourseTAJunction(5, self.course.pk, self.ta.pk).save()
        response = self.client.post("/labs/", {"ta": "bad name", "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Incorrect message for invalid entry for ta already in course"
        self.assertEqual(response.context['message'], "user or lab not found", msg=failure_msg)

    def test_valid_entry_TA_in_course_db(self):
        CourseTAJunction(5, self.course.pk, self.ta.pk).save()
        self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "There should not be a new entry for TA Course Junction"
        self.assertEqual(self.length + 1, len(CourseTAJunction.objects.all()), msg=failure_msg)

    def test_valid_entry_TA_not_in_course_message(self):
        response = self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Incorrect message for valid entry for ta already in course"
        self.assertEqual(response.context['message'], "TA assigned to lab and course", msg=failure_msg)

    def test_valid_entry_TA_not_in_course_db(self):
        self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "new entry not added for assigning TA to a course"
        self.assertEqual(LabTAJunction.objects.get(user_id=self.ta).lab_id, self.lab, msg=failure_msg)

    def test_valid_two_TA_valid(self):
        user_ta_2 = User(912, "V", "", "", "", 1, "")
        user_ta_2.save()
        self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        self.client.post("/labs/", {"ta": user_ta_2.name, "labs": self.lab.lab_name}, follow=True)
        users = []
        for e in LabTAJunction.objects.filter(lab_id=self.lab):
            users.append(e.user_id)
        failure_msg = "2 TAs should be assigned to the Lab"
        self.assertEqual(users, [self.ta, user_ta_2], msg=failure_msg)

    def test_attempt_add_admin_message(self):
        user_admin = User(955, "Terrance", "", "", "", 3, "")
        user_admin.save()
        response = self.client.post("/labs/", {"ta": user_admin.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Incorrect message when not trying to add an Amin to a lab"
        self.assertEqual(response.context['message'], "Only TA can be added to lab", msg=failure_msg)

    def test_attempt_add_admin_db(self):
        user_instr = User(955, "Terrance", "", "", "", 3, "")
        user_instr.save()
        self.client.post("/labs/", {"ta": user_instr.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Should not be able to add an instructor to a lab"
        self.assertEqual(self.length, len(LabTAJunction.objects.all()), msg=failure_msg)

    def test_attempt_add_instr_message(self):
        user_admin = User(955, "Terrance", "", "", "", 3, "")
        user_admin.save()
        length = len(LabTAJunction.objects.all())
        self.client.post("/labs/", {"ta": user_admin.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Incorrect message when not trying to add an Instructor to a lab"
        self.assertEqual(length, len(LabTAJunction.objects.all()), msg=failure_msg)

    def test_attempt_add_instr_db(self):
        user_instr = User(955, "Terrance", "", "", "", 2, "")
        user_instr.save()
        length = len(LabTAJunction.objects.all())
        self.client.post("/labs/", {"ta": user_instr.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Should not be able to add an instructor to a lab"
        self.assertEqual(length, len(LabTAJunction.objects.all()), msg=failure_msg)

    def test_empty_fields(self):
        failure_msg = "Added to DB despite empty field"
        self.client.post("/labs/", {"ta": "", "labs": ""}, follow=True)
        self.assertEqual(self.length, len(LabTAJunction.objects.all()), msg=failure_msg)

        self.client.post("/labs/", {"ta": "", "labs": self.lab.lab_name}, follow=True)
        self.assertEqual(self.length, len(LabTAJunction.objects.all()), msg=failure_msg)

        self.client.post("/labs/", {"ta": self.ta.name, "labs": ""}, follow=True)
        self.assertEqual(self.length, len(LabTAJunction.objects.all()), msg=failure_msg)

    def test_double_ta_name(self):
        User(59, "New TA Name", "password", "email@gmail.com", "address", 1, "51352056").save()
        response = self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Double ta name message not correct"
        self.assertEqual(response.context['message'], "TA assigned to lab and course", msg=failure_msg)

    def test_double_lab_name(self):
        self.lab = Lab(14, "Lab", "description")
        self.lab.save()
        LabCourseJunction(8, self.lab.pk, self.course.pk).save()
        response = self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Double lab name not correct"
        self.assertEqual(response.context['message'], "TA assigned to lab and course", msg=failure_msg)


class TestOtherUserCreateLab(TestCase):
    def setUp(self):
        self.ta = User(56, "New TA Name", "password", "email@gmail.com", "address", 1, "51352056")
        self.ta.save()
        # User.objects.create(3, "New TA 2", "password2", "email2@gmail.com", "address2", 1, "513520562")
        instr = User(4, "Instructor", "password2", "email3@gmail.com", "address3", 2, "563520562")
        instr.save()
        self.course = Course(16, "CS150", instr.pk, "meeting time", "fall", "course type", "description")
        self.course.save()
        self.lab = Lab(16, "Lab", "description")
        self.lab.save()
        LabCourseJunction(5, self.lab.pk, self.course.pk).save()
        self.firstResponse = self.client.post("/", {"email": "testAdmin@test.com", "password": "tA1!"}, follow=True)
        self.length = len(LabTAJunction.objects.all())

    def test_ta_attempt_message(self):
        self.client.post("/", {"email": "email@gmail.com", "password": "password"}, follow=True)
        response = self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Incorrect message for TA attempt to add a TA to a lab"
        self.assertEqual("You must be an Admin to add a TA to a Lab", response.context['message'], msg=failure_msg)

    def test_TA_attempt_db_changes(self):
        self.client.post("/", {"email": "email@gmail.com", "password": "password"}, follow=True)
        self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Database entry should not be added for TA attempt to add a TA to a lab"
        self.assertEqual(self.length, len(LabTAJunction.objects.all()), msg=failure_msg)

    def test_instructor_attempt_message(self):
        self.client.post("/", {"email": "email3@gmail.com", "password": "password2"}, follow=True)
        response = self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Incorrect message for Instructor attempt to add a TA to a lab"
        self.assertEqual("You must be an Admin to add a TA to a Lab", response.context['message'], msg=failure_msg)

    def test_instructor_attempt_db_changes(self):
        self.client.post("/", {"email": "email3@gmail.com", "password": "password2"}, follow=True)
        self.client.post("/labs/", {"ta": self.ta.name, "labs": self.lab.lab_name}, follow=True)
        failure_msg = "Database entry should not be added for Instructor attempt to add a TA to a lab"
        self.assertEqual(self.length, len(LabTAJunction.objects.all()), msg=failure_msg)
