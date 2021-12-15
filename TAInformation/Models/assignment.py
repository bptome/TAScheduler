from TAInformation.Models.instructor import Instructor
from TAInformation.Models.taAssignment import taAssignment


class ClassAssignment:
    def __init__(self, course: str, assignment: str, TA: str):
        self.course = course
        self.assignment = assignment
        self.TA = TA

