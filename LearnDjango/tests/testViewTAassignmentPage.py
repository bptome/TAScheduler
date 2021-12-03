from django.test import TestCase
from django.test import Client
from .model import User
from .model import Course
from .model import Lab


class viewAssignmentPage(TestCase):
    client = None
    things = None

    def setUp(self):
        self.client = Client()

        user = User(
            user_id="1", name="ze", password="1234", email="ze@uwm.edu", home_address="01 s milwaukee",
            role="1", phone="23456"
        )
        user.save()

        courseList = Course(
            course_id="03", course_name="CS", instructor_id="0234", lab="None",
            meeting_time="monday: 2pm-3pm",
            semester="fall 2021", course_type="online", description="2nd and 3rd year level course"
        )
        courseList.save()

        labDescription = Lab(
            lab_id="023", lab_name="CS", ta_id="123", course_id="03", has_grader=" False",
            description=" This class has a lab that helps the student to increase their logical thinking skills"
        )
        labDescription.save()

    def test_homepage(self):
        # ACT

        r = self.client.post("/", {"lab_id": "023", "lab_name": "CS", "ta_id": "123", "course_id": "03",
                                   "has_grader": " False",

                                   "description": "this class has a lab that helps the student to increase their "
                                                  "logical thinking skills"},
                             follow=True)
        # Arrange
        self.assertEqual("CS", r.context["lab_name"], msg=" Correct the homepage is displayed the list of the course ")

    # check atleast one TA is active
    def test_activeTA(self):
        # ACT

        r = self.client.post("/", {"lab_id": "023", "lab_name": "CS", "ta_id": "123", "course_id": "03",
                                   "has_grader": " False",

                                   "description": "This class has a lab that helps the student to increase their "
                                                  "logical thinking skills"},
                             follow=True)
        # Arrange
        self.assertEqual("123", r.context["ta_id"], msg=" correct the at least one TA is active")

    def test_NotActiveTA(self):
        # ACT

        r = self.client.post("/", {"lab_id": "023", "lab_name": "CS", "ta_id": "123", "course_id": "03",
                                   "has_grader": " False",

                                   "description": "This class has a lab that helps the student to increase their "
                                                  "logical thinking skills"},
                             follow=True)
        # Arrange
        self.assertEqual("", r.context["ta_id"], msg=" correct the at least one TA is active")

    # check the name of TA corresponding to the assigned course
    def test_nameListTA(self):
        # ACT
        r = self.client.post("/", {"user_id": "1", "name": "ze", "password": "1234", "email": "ze@uwm.edu",
                                   "home_address": "01 s milwaukee", "role": "1", "phone": "23456"}, follow=True)
        # Arrange
        self.assertEqual("ze", r.context["name"], msg=" one of the TA name from the list ")

    # check the lab are published
    def test_lab_published(self):
        # ACT
        r = self.client.post("/", {"lab_id": "023", "lab_name": "CS", "ta_id": "123", "course_id": "03",
                                   "has_grader": " False",
                                   "description": "this class has a lab that helps the student to increase their "
                                                  "logical thinking skills"},
                             follow=True)
        # Arrange
        self.assertEqual("023", r.context["lab_id"], msg=" the lab is published and it is visible for all student")

    def test_lab_NotPublished(self):
        # ACT
        r = self.client.post("/", {"lab_id": "023", "lab_name": "CS", "ta_id": "123", "course_id": "03",
                                   "has_grader": " False",
                                   "description": "this class has a lab that helps the student to increase their "
                                                  "logical thinking skills"},
                             follow=True)
        # Arrange
        self.assertEqual('', r.context["lab_id"], msg=" the lab is published and it is visible for all student")

    # check the single course assignment
    def test_assignCourseTa(self):
        # ACT
        r = self.client.post("/", {"course_id": "03", "course_name": "CS", "instructor_id": "0234",
                                   "lab": "None", "meeting_time": "monday 2pm-3pm",
                                   "semester": "fall 2021", "course_type": "online",
                                   "description": "2nd and 3rd year level course"}, follow=True)
        # Arrange
        self.assertEqual("CS", r.context["course_name"], msg=" This course is assigned to the TA_ID number 123")

    # check the disable assignment
    def test_viewDisableAssignment(self):
        # ACT

        r = self.client.post("/", {"lab_id": "023", "lab_name": "CS", "ta_id": "123", "course_id": "03",
                                   "has_grader": " False",

                                   "description": "this class has a lab that helps the student to increase their "
                                                  "logical thinking skills"},
                             follow=True)
        # Arrange
        self.assertEqual("", r.context["lab_name"],
                         msg=" The course is not available any more in the course home page ")

    # check if the course is available
    def test_CoursNotAvailable(self):
        # ACT

        r = self.client.post("/", {"lab_id": "023", "lab_name": "CF", "ta_id": "123", "course_id": "03",
                                   "description": "this class has a lab that helps the student to increase their "
                                                  "logical thinking skills",

                                   "has_grader": " False"},
                             follow=True)
        # Arrange
        self.assertEqual("CF", r.context["lab_name"], msg=" Incorrect the course is not available yet")

    def test_CoursAvailable(self):
        # ACT

        r = self.client.post("/", {"lab_id": "023", "lab_name": "CS", "ta_id": "123", "course_id": "03",
                                   "description": "this class has a lab that helps the student to increase their "
                                                  "logical thinking skills",

                                   "has_grader": " False"},
                             follow=True)
        # Arrange
        self.assertEqual("CS", r.context["lab_name"], msg=" Incorrect the course is not available yet")
