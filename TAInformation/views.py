from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View

from TAInformation.Models.account_type import AccountType
from TAInformation.Models.admin import UserAdmin
from TAInformation.Models.base_user import BaseUser
from TAInformation.Models.instructor import Instructor
from TAInformation.Models.ta import TA
from TAInformation.models import User, Course, Lab, LabCourseJunction


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
            # items from database to present with
            userInDb = User(user_id=10, name="Vee", password="pass", email="test@email.com",
                            home_address="3438 tree lane", role=3, phone="123456789")
            userInDb.save()

            newInstructor = User(user_id=11, name="Sam", password="password", email="ta@email.com",
                                 home_address="7867 tea tree lane", role=2, phone="234567891")
            newInstructor.save()
            User(98, "Henry Trimbach", "ter7ythg", "trimbach@uwm.edu", "Downer ave", 2, "(414)143-4867").save()
            Course(3, "CS351", 98, "W 900:00-6:00", "Fall", "Graduate", "EZ").save()
            Lab(1, "Lab 900", False, "boring lab").save()
            LabCourseJunction(2, 1, 3).save()
            Lab(2, "Lab 901", False, "not boring lab").save()
            LabCourseJunction(3, 2, 3).save()
            user = User.objects.get(email=request.POST['email'])
            request.session["user_id"] = user.user_id
            request.session["email"] = user.email
            request.session["role"] = user.role
            if (user == None):
                return render(request, "login.html", {"message": "no such account, please try again"})
            badPassword = (user.password != request.POST['password'])
        except:
            noSuchUser = True

        if (user != None and (not badPassword) and validatePassword(self, request.POST[
            'password'])):
            return redirect("/dashboard/")

        elif badPassword:
            return render(request, "login.html", {"message": "wrong password, please try again"})
        elif noSuchUser:
            return render(request, "login.html", {"message": "no such account, please try again"})



class DashBoard(View):
    def get(self, request):
        return render(request, "dashboard.html", {})


class Courses(View):
    def get(self, request):
        m = get_user(request.session["user_id"])

        avaliableInstructors = []
        for temp in User.objects.filter(role=AccountType.INSTRUCTOR.value).values():
            avaliableInstructors.append(temp["name"])

        return render(request, "courses.html", {"name": m.name, "courses": m.display_courses(), "avaliableInstructors": avaliableInstructors})
    def post(self, request):
        m = get_user(request.session["user_id"])
        noPermissions = canAccess(m.role, AccountType.ADMIN.value)  # User.objects.get('role')
        if noPermissions:
            return render(request, "courses.html",
                          {"message": "insufficent permissions to create a course. Please contact "
                                      "your system administrator if you believe this is in error."})
        else:
          newCourse = addCourse(request.POST['name'], request.POST['instructor'],
                                  request.POST['meeting_time'], request.POST['semester'], request.POST['course_type'],
                                  request.POST['description'])
        newCourse.save()
        return render(request, "courses.html", {"name": m.name, "courses": m.display_courses(), "message": "Course Created Successfully"})



class People(View):
    def get(self, request):
        m = get_user(request.session["user_id"])
        return render(request, "people.html", {"name": m.name, "people": m.display_people(),
                                               "labels": m.display_people_fields()})
        
        
# For create account web pages
class CreateUser(View):
    # Precondition: User is logged in and data is stored in session
    # Postcondition: Page with Create Course form is displayed
    # Side Effects: None
    def get(self, request):
        return render(request, "create_user.html", {})

    # Precondition: User has entered data in all form fields in proper format
    # Postcondition: Creates new user, if data entered validates successfully and user doesn’t already exist.
    # Side Effects: Message indicating result is displayed at the bottom of the “Create Courses” form
    def post(self, request):
        # Extract data from form
        # match request.session['role']:
        #     case AccountType.ADMIN.value:
        #         current_user = UserAdmin(
        #             int(request.session['user_id']),
        #             "",
        #             "",
        #             request.session['email'],
        #             "",
        #             ""
        #         )
        #     case AccountType.INSTRUCTOR.value:
        #         current_user = Instructor(
        #             int(request.session['user_id']),
        #             "",
        #             "",
        #             request.session['email'],
        #             "",
        #             ""
        #         )
        #     case AccountType.TA.value:
        #         current_user = TA(
        #             int(request.session['user_id']),
        #             "",
        #             "",
        #             request.session['email'],
        #             "",
        #             ""
        #         )
        #     case _:
        #         current_user: BaseUser

        result_dict = {}
        the_id = -1 if request.POST.get('user_id') == "" else int(request.POST.get('user_id'))

        # match int(request.POST.get('role')):
        #     case 1:
        #         new_user = TA(
        #             the_id,
        #             request.POST.get('name'),
        #             request.POST.get('password'),
        #             request.POST.get('email'),
        #             request.POST.get('address'),
        #             request.POST.get('phone'),
        #         )
        #     case 2:
        #         new_user = Instructor(
        #             the_id,
        #             request.POST.get('name'),
        #             request.POST.get('password'),
        #             request.POST.get('email'),
        #             request.POST.get('address'),
        #             request.POST.get('phone'),
        #         )
        #     case 3:
        #         new_user = UserAdmin(
        #             the_id,
        #             request.POST.get('name'),
        #             request.POST.get('password'),
        #             request.POST.get('email'),
        #             request.POST.get('address'),
        #             request.POST.get('phone')
        #         )
        #     case _:  # Enforcement of selection should never allow this case to be reached
        #         new_user: BaseUser
        #
        # result_dict = current_user.create_user(new_user)

        return render(request, "create_user.html", {'result': result_dict['result'], 'message': result_dict['message']})
      
           
# this is a dummy method. will eventually use user_id and return a User() class of the user that matches the user_id
def findUser(name):
    # b = User.objects.filter(name=name)
    User(1, "Bryce Tome", "sfG76Fgh", "bptome@uwm.edu", "fake address 566", 1, "(414)546-3464").save()
    return User(1, "Bryce Tome", "sfG76Fgh", "bptome@uwm.edu", "fake address 566", 1, "(414)546-3464")  # b.user_id


# this is a helper method. will eventually use role required & current role to return true if can be accessed, and false if insufficient permissions
def canAccess(role, required_role):
    return False


# helper method to take all data from user and return a Course() class instance. This method also generates a user_id for each course
def addCourse(course_name, instructor_name, meeting_time, semester, course_type, description):
    newCourse = Course(course_name=course_name, instructor_id=findUser(instructor_name),
                       meeting_time=meeting_time, semester=semester, course_type=course_type, description=description)
    return newCourse

  
# helper method to take password string and return boolean. This method tests if password string is valid
def validatePassword(self, password):
    if password.isspace() or len(password) < 1:
        return False
    return True

class Labs(View):
    def get(self, request):
        return render(request, "labs.html")

