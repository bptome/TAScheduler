from django.test import TestCase
from django.test import Client
from TAInformation.models import Course, User
from TAInformation.models import taAssignment, courseName


class testAssignment(TestCase):
    client = None
    Assignment = None

    def setUp(self):
        user = taAssignment(
            Course='CS', Assignment='HW_2', TA='Zack'
        )
        user.save()
        self.client = Client()

    def test_rightTA(self):
        #Act
        r = self.client.post("/", {"Course": "CS", "Assignment": "HW_2", "TA": "Zack"}, follow=True)
        #assert
        self.assertEqual("Zack", r.context["TA"], msg=" cs hW_2 assigned to Zack(TA)")

    def test_wrongTa(self):
        #Act
        r = self.client.post("/", {"Course": "CS", "Assignment": "HW_2", "TA": ""}, follow=True)
        #assert
        self.assertEqual("", r.context["TA"], msg=" The TA name is doesn't show up ")

    def test_course(self):
        #Act
        r = self.client.post("/", {"Course": "CS", "Assignment": "HW_2", "TA": "Zack"}, follow=True)
        #asset
        self.assertEqual("CS", r.context["Course"], msg=" the assignment course list displayed")

    def test_wrongCourse(self):
        #Act
        r = self.client.post("/", {"Course": "", "Assignment": "HW_2", "TA": "Zack"}, follow=True)
        #asset
        self.assertEqual("", r.context["Course"], msg=" Course doesn't show app ")

    def test_assignment(self):
        #Act
        r = self.client.post("/", {"Course": "CS", "Assignment": "HW_2", "TA": "Zack"}, follow=True)
        #asset
        self.assertEqual("HW_2", r.context["Assignment"], msg=" CS  HW_2 is available  ")

    def test_wrongAssignment(self):
        #Act
        r = self.client.post("/", {"Course": "", "Assignment": "", "TA": "Zack"}, follow=True)
        #asset
        self.assertEqual("", r.context["Assignment"], msg=" Assignment doesn't show up ")

    def test_disableAssignment(self):
        #Act
        r = self.client.post("/", {"Course": "", "Assignment": "", "TA": "Zack"}, follow=True)
        #asset
        self.assertEqual("", r.context["Assignment"], msg=" Assignment is disable ")
