from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.views import View

from TAInformation.models import User


def index(request):
    return HttpResponse("Hello , world. You're at the polls index.")


class Home(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        return render(request, "createCourse.html",
                      {"message": "User Created Sucsessfully"})
class Course(View):

    def get(self, request):
        return render(request, "createCourse.html", {})

    def post(self, request):
        noPermissions = canAccess(User.objects.get('role'), 1)

        if noPermissions:
            return render(request, "createCourse.html",
                          {"message": "insufficent permissions to create a course. Please contact "
                                      "your system administrator if you believe this is in error."})
        else:
            newCourse = addCourse(request.POST['name'], request.POST['instructor'], request.POST['lab'], request.POST['meeting_time'], request.POST['semester'], request.POST['course_type'], request.POST['description'])
            newCourse.save()
            request.session["name"] = newCourse.name
            return redirect("/")


#this is a dummy method. will eventually use user_id and return a User() class of the user that matches the user_id
def findUser(name):
    b = User.objects.filter(name=name)
    return b.user_id

#this is a helper method. will eventually use role required & current role to return true if can be accessed, and false if insufficient permissions
def canAccess(role, required_role):

#helper method to take all data from user and return a Course() class instance. This method also generates a user_id for each course
def addCourse(self, course_name, instructor_name, lab, meeting_time, semester, course_type, description):
    newCourse = Course(course_name=course_name, instructor_id=findUser(instructor_name), lab=lab,
                       meeting_time=meeting_time, semester=semester, course_type=course_type, description=description)
    return newCourse


