from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View

from TAInformation.Models.account_type import AccountType
from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.base_user import BaseUser
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.models import User, Course


def get_user(my_user_id: int):
    m = User.objects.get(user_id=my_user_id)
    role = m.role
    if role == AccountType.DEFAULT.value:
        return BaseUser(m.user_id, m.name, m.password, m.email, m.home_address, m.phone)
    elif role == AccountType.TA.value:
        return TA(m.user_id, m.name, m.password, m.email, m.home_address, m.phone)
    elif role == AccountType.INSTRUCTOR.value:
        return Instructor(m.user_id, m.name, m.password, m.email, m.home_address, m.phone)
    elif role == AccountType.ADMIN.value:
        return UserAdmin(m.user_id, m.name, m.password, m.email, m.home_address, m.phone)
    return AccountType.ADMIN.value


def index(request):
    return HttpResponse("Hello , world. You're at the polls index.")


class Home(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        badPassword = False
        user = None
        noSuchUser = False
        try:
            #items from database to present with
            userInDb = User(user_id=10, name="Vee", password="pass", email="test@email.com", home_address="3438 tree lane", role=1, phone="123456789")
            userInDb.save()
            newInstructor = User(user_id=11, name="Sam", password="password", email="ta@email.com", home_address="7867 tea tree lane", role=1, phone="234567891")
            newInstructor.save()
            newCourse = addCourse(course_id=1, course_name="Lit 101", instructor_id=11, meeting_time="TR 10:00-10:30am", semester="fall 2021", course_type="online", description="n/a")
            newCourse.save()

            user = User.objects.get(email=request.POST['email'])
            if (user == None):
                return render(request, "login.html", {"message": "no such account, please try again"})
            badPassword = (user.password != request.POST['password'])
            request.session["user_id"] = user.user_id
            request.session["email"] = user.email
            request.session["role"] = user.role
        except:
            noSuchUser = True

        if ((not badPassword) and validatePassword(self,request.POST['password'])):
            return redirect("/dashboard/")

        elif badPassword:
            return render(request, "login.html", {"message": "wrong password, please try again"})
        elif noSuchUser:
            return render(request, "login.html", {"message": "no such account, please try again"})

        # render(request, "createCourse.html",
        # {"message": "User Created Sucsessfully"})


class DashBoard(View):
    def get(self, request):
        return render(request, "dashboard.html", {})


class Courses(View):
    def get(self, request):
        m = get_user(request.session["user_id"])

        return render(request, "courses.html", {"name": m.name, "courses": m.display_courses()})


class People(View):
    def get(self, request):
        m = get_user(request.session["user_id"])
        return render(request, "people.html", {"name": m.name, "people": m.display_people(),
                                               "labels": m.display_people_fields()})


class AddCourse(View):
    def get(self, request):
        return render(request, "createCourse.html", {})

    def post(self, request):
        noPermissions = canAccess(User.objects.get('role'), 1)

        if noPermissions:
            return render(request, "createCourse.html",
                          {"message": "insufficent permissions to create a course. Please contact "
                                      "your system administrator if you believe this is in error."})
        else:
            newCourse = addCourse(request.POST['name'], request.POST['instructor'], request.POST['lab'],
                                  request.POST['meeting_time'], request.POST['semester'], request.POST['course_type'],
                                  request.POST['description'])
            newCourse.save()
            request.session["name"] = newCourse.name
            return redirect("/dashboard/")


# this is a dummy method. will eventually use user_id and return a User() class of the user that matches the user_id
def findUser(name):
    b = User.objects.filter(name=name)
    return b.user_id


# this is a helper method. will eventually use role required & current role to return true if can be accessed, and false if insufficient permissions
def canAccess(role, required_role):
    return


# helper method to take all data from user and return a Course() class instance. This method also generates a user_id for each course
def addCourse(self, course_name, instructor_name, lab, meeting_time, semester, course_type, description):
    newCourse = Course(course_name=course_name, instructor_id=findUser(instructor_name), lab=lab,
                       meeting_time=meeting_time, semester=semester, course_type=course_type, description=description)
    return newCourse

# helper method to take password string and return boolean. This method tests if password string is valid
def validatePassword(self, password):
   if(password.isspace() or len(password)<1):
       return False
   return True
