from abc import abstractmethod

from django.db import models


# Create your models here.

class User(models.Model):
    user_id = models.IntegerField(default=1)
    name = models.CharField(max_length=20, default='email')
    password = models.CharField(max_length=20, default='email')
    email = models.EmailField(max_length=20, default='email')  # models.EmailField(max_length=20)
    home_address = models.CharField(max_length=20, default='"101 W. Wisconsin Ave, Milwaukee, WI 53203"')
    role = models.IntegerField(default=1)
    phone = models.IntegerField(default=123)


class Course(models.Model):
    course_id = models.IntegerField()
    course_name = models.CharField(max_length=20)
    instructor_id = models.IntegerField()
    lab = models.CharField(max_length=20)  # TODO: Needs to be an int array!
    meeting_time = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    course_type = models.CharField(max_length=20)
    description = models.CharField(max_length=200)


class Lab(models.Model):
    lab_id = models.IntegerField()
    lab_name = models.CharField(max_length=20)
    ta_id = models.IntegerField()
    course_id = models.IntegerField()
    has_grader = models.BooleanField()
    description = models.CharField(max_length=200)
