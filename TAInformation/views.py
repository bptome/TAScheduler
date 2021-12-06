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
        # this is an example code
        request.session["user_id"] = 1
        return redirect("/courses/")


class Courses(View):
    def get(self, request):
        m = get_user(request.session["user_id"])
        return render(request, "courses.html", {"name": m.name, "courses": m.display_courses()})

class People(View):
    def get(self, request):
        m = get_user(request.session["user_id"])
        return render(request, "people.html", {"name": m.name, "people": m.display_people(),
                                               "labels": m.display_people_fields()})

def Course1(View):
    def get(self, request):
        return render(request, "Course.html", {})

    def post(self, request):
        m = User.objects.get(name=request.POST['role'])
        noPermissions = (m.role != 1)
        # except:
        #     noSuchUser = True
        # if noSuchUser:
        #     m = User(name=request.POST['name'], password = request.POST['password'])
        #     m.save()
        #     request.session["name"] = m.name
        #     return redirect("/things/")
        if noPermissions:
            return render(request, "home.html",
                          {"message": "insufficent permissions to create a course. Please contact "
                                      "your system administrator if you believe this is in error."})
        else:
            m = Course(course_name=request.POST['course_name'], )
            m.save()
            request.session["name"] = m.name
            return redirect("/things/")
