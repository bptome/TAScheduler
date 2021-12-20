from django.test import TestCase
from django.test import Client
from TAInformation.models import Course, User, CourseTAJunction


class testAssignment(TestCase):

    def setUp(self):
        user = CourseTAJunction(
            Course='CS361', TA='Zack'
        )
        user.save()
        self.client = Client()

    def test_rightTA(self):
        # Act
        r = self.client.post("/", {"Course": "CS361", "TA": "Zack"}, follow=True)
        # assert
        self.assertEqual("Zack", r.context["TA"], msg=" CS361 assigned to Zack(TA)")

    def test_wrongTa(self):
        # Act
        r = self.client.post("/", {"Course": "CS361", "TA": ""}, follow=True)
        # assert
        self.assertEqual("", r.context["TA"], msg=" The TA name is doesn't show up ")

    def test_course(self):
        # Act
        r = self.client.post("/", {"Course": "CS361", "TA": "Zack"}, follow=True)
        # asset
        self.assertEqual("CS361", r.context["Course"], msg=" The assignment course list displayed")

    def test_wrongCourse(self):
        # Act
        r = self.client.post("/", {"Course": "", "TA": "Zack"}, follow=True)
        # asset
        self.assertEqual("", r.context["Course"], msg=" Course doesn't show app ")

    def test_disableAssignment(self):
        # Act
        r = self.client.post("/", {"Course": "CS361", "TA": "Zack"}, follow=True)
        # asset
        self.assertEqual("", r.context["Course"], msg=" Assignment is disable ")
