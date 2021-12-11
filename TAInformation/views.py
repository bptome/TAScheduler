from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.views import View

from TAInformation.Models.account_type import AccountType
from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.base_user import BaseUser
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.models import User


def index(request):
    return HttpResponse("Hello , world. You're at the polls index.")


class Home(View):
    def get(self, request):
        return render(request, "login.html", {})


class Course(View):
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


# For create account web pages
class CreateUser(View):
    # Precondition: User is logged in and data is stored in session
    # Postcondition: Page with Create Course form is displayed
    # Side Effects: None
    def get(self, request):
        # request.session['currentUserID'] = 1
        # request.session['currentName'] = "Terence"
        # request.session['currentPassword'] = ""
        # request.session['currentEmail'] = ""
        # request.session['currentAddress'] = ""
        # request.session['currentPhone'] = ""
        # request.session['currentRole'] = AccountType.ADMIN.value
        return render(request, "create_user.html", {})

    # Precondition: User has entered data in all form fields in proper format
    # Postcondition: Creates new user, if data entered validates successfully and user doesn’t already exist.
    # Side Effects: Message indicating result is displayed at the bottom of the “Create Courses” form
    def post(self, request):
        # Extract data from form
        match request.session['role']:
            case AccountType.ADMIN.value:
                current_user = UserAdmin(
                    int(request.session['user_id']),
                    "",
                    "",
                    request.session['email'],
                    "",
                    ""
                )
            case AccountType.INSTRUCTOR.value:
                current_user = Instructor(
                    int(request.session['user_id']),
                    "",
                    "",
                    request.session['email'],
                    "",
                    ""
                )
            case AccountType.TA.value:
                current_user = TA(
                    int(request.session['user_id']),
                    "",
                    "",
                    request.session['email'],
                    "",
                    ""
                )
            case _:
                current_user: BaseUser

        result_dict = {}
        the_id = -1 if request.POST.get('user_id') == "" else int(request.POST.get('user_id'))
        match int(request.POST.get('role')):
            case 1:
                new_user = TA(
                    the_id,
                    request.POST.get('name'),
                    request.POST.get('password'),
                    request.POST.get('email'),
                    request.POST.get('address'),
                    request.POST.get('phone'),
                )
            case 2:
                new_user = Instructor(
                    the_id,
                    request.POST.get('name'),
                    request.POST.get('password'),
                    request.POST.get('email'),
                    request.POST.get('address'),
                    request.POST.get('phone'),
                )
            case 3:
                new_user = UserAdmin(
                    the_id,
                    request.POST.get('name'),
                    request.POST.get('password'),
                    request.POST.get('email'),
                    request.POST.get('address'),
                    request.POST.get('phone')
                )
            case _:  # Enforcement of selection should never allow this case to be reached
                new_user: BaseUser

        result_dict = current_user.create_user(new_user)

        return render(request, "create_user.html", {'result': result_dict['result'], 'message': result_dict['message']})
