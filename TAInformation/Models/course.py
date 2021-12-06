from TAInformation.Models.instructor import Instructor
from TAInformation.Models.lab import CourseLab


class ClassCourse:
    def __init__(self, id_number: int, name: str, instructor: Instructor, lab: str,
                 meeting_time: str, semester: str, course_type: str, description: str):
        self.course_id = id_number
        self.course_name = name
        self.instructor = instructor
        self.lab = lab
        self.meeting_time = meeting_time
        self.semester = semester
        self.course_type = course_type
        self.description = description
