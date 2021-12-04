import none as none
from django.test import TestCase, Client

from TAInformation.models import Course, User


class TestCreateCourses(TestCase):
    def setUp(self):
        self.client = Client()
        self.defaultCourse = Course(none,
                                    {"course_name": "english", "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": "Spring 2022"})

        self.noNameCourse = Course(none, {"course_name": none, "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                          "semester": "Spring 2022"})
        self.user = User(1, "testAdmin", "tA1!", "testAdmin@test.com", "101 W. Wisconsin Ave, Milwaukee, WI 53203",

                         "(414)222-2571")

    def test_default(self):
        response = self.client.post("/course",
                                    {"course_name": "english", "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": "Spring 2022"}, follow=True)
        self.assertEqual(
            self.Course.addCourse({"course_name": "english", "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                   "semester": "Spring 2022"}), response)

    def test_no_name(self):
        response = self.client.post("/course",
                                    {"course_name": none, "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
                                     "semester": "Spring 2022"}, follow=True)
        failure_msg = "please enter a name to create a course. Please contact your system administrator if you " \
                      "believe this is in error. "
        self.assertEqual(response.context["message"], self.Course.addCourse(
            {"course_name": none, "instructor_id": 1, "meeting_time": "M-W 1:00 - 2:15",
             "semester": "Spring 2022"}), msg=failure_msg)

    # instructor_id = models.IntegerField()
    # lab = models.CharField(max_length=20)  # TODO: Needs to be an int array!
    # meeting_time = models.CharField(max_length=20)
    # semester = models.CharField(max_length=20)
    # course_type = models.CharField(max_length=20)
    # description = models.CharField(max_length=200)}
