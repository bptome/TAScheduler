import sys

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

    match m.role:
        case AccountType.TA.value:
            return TA(m.user_id, m.name, m.password, m.email, m.home_address, m.phone)
        case AccountType.INSTRUCTOR.value:
            return Instructor(m.user_id, m.name, m.password, m.email, m.home_address, m.phone)
        case AccountType.ADMIN.value:
            return UserAdmin(m.user_id, m.name, m.password, m.email, m.home_address, m.phone)
        case _:
            return BaseUser(m.user_id, m.name, m.password, m.email, m.home_address, m.phone)


def index(request):
    return HttpResponse("Hello , world. You're at the polls index.")


class Home(View):
    def get(self, request):
        request.session["user_id"] = None
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
            User(99, "Jane Doe", "apple", "doe@uwm.edu", "Random ave", 1, "(123)143-4867").save()
            User(98, "Henry Trimbach", "ter7ythg", "trimbach@uwm.edu", "Downer ave", 2, "(414)143-4867").save()
            User(98, "New TA", "ter7ythg", "trimbach@uwm.edu", "Downer ave", 1, "(414)143-4867").save()
            Course(3, "CS351", 98, "W 900:00-6:00", "Fall", "Graduate", "EZ").save()
            Course(4, "CS250", 99, "W 900:00-6:00", "Summer", "Graduate", "ONLINE").save()
            Lab(1, "Lab 900", "boring lab").save()
            LabCourseJunction(2, 1, 3).save()
            Lab(2, "Lab 901", "not boring lab").save()
            LabCourseJunction(3, 2, 3).save()

            if 'email' in request.POST:
                user = User.objects.get(email=request.POST['email'])
            if user is not None:
                request.session["user_id"] = user.user_id
                request.session["email"] = user.email
                request.session["role"] = user.role
            if user == None:
                return render(request, "login.html", {"message": "no such account, please try again"})
            badPassword = (user.password != request.POST['password'])
        except:
            print("%s - %s at line: %s" % (sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
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
        if (request.session["user_id"] == None):
            return render(request, "login.html", {"message": "you do not have access to this page"})
        m = User.objects.get(user_id=request.session["user_id"])
        return render(request, "dashboard.html", {"name": m.name})


class Courses(View):
    def get(self, request):
        if (request.session["user_id"] == None):
            return render(request, "login.html", {"message": "you do not have access to this page"})

        m = get_user(request.session["user_id"])

        return render(request, "courses.html", {"name": m.name, "role": m.role, "courses": m.display_courses(),
                                                "avaliableInstructors": m.avaliableInstructors(),
                                                "avaliableTAs": m.avaliableTAs(),
                                                "avaliableCourses": m.avaliableCourses()})

    def post(self, request):
        m = get_user(request.session["user_id"])

        if 'addToCourse' in request.POST:
            user_name = request.POST.get('ta', False);
            course_name = request.POST.get('course', False);
            if User.objects.filter(name=user_name).exists() & Course.objects.filter(course_name=course_name).exists():
                user_object = User.objects.get(name=user_name)
                course_object = Course.objects.get(course_name=course_name)
                return render(request, "courses.html",
                              {"message": m.assign_ta_to_course(user_object, course_object),
                               "avaliableInstructors": m.avaliableInstructors(), "avaliableTAs": m.avaliableTAs(),
                               "avaliableCourses": m.avaliableCourses(), "name": m.name, "role": m.role, })

            return render(request, "courses.html",
                          {"message": "TA or Course not found", "avaliableInstructors": m.avaliableInstructors(),
                           "avaliableTAs": m.avaliableTAs(), "avaliableCourses": m.avaliableCourses(), "name": m.name,
                           "role": m.role, })

        noPermissions = canAccess(m.role, AccountType.ADMIN.value)  # User.objects.get('role')
        if noPermissions:
            newCourse = addCourse(request.POST['name'], request.POST['instructor'],
                                  request.POST['meeting_time'], request.POST['semester'], request.POST['course_type'],
                                  request.POST['description'])

            newCourse.save()
            return render(request, "courses.html", {"name": m.name, "role": m.role, "courses": m.display_courses(),
                                                    "message": "Course Created Successfully",
                                                    "avaliableInstructors": m.avaliableInstructors(),
                                                    "avaliableTAs": m.avaliableTAs(),
                                                    "avaliableCourses": m.avaliableCourses()})
        else:
            return render(request, "courses.html",
                          {"message": "insufficent permissions to create a course. Please contact "
                                      "your system administrator if you believe this is in error.",
                           "avaliableInstructors": m.avaliableInstructors(), "avaliableTAs": m.avaliableTAs(),
                           "avaliableCourses": m.avaliableCourses()})


class People(View):
    def get(self, request):
        if (request.session["user_id"] == None):
            return render(request, "login.html", {"message": "you do not have access to this page"})

        m = get_user(request.session["user_id"])
        return render(request, "people.html", {"name": m.name, "role": m.role, "people": m.display_people(),
                                               "labels": m.display_people_fields()})


# For create account web pages
class CreateUser(View):
    # Precondition: User is logged in and data is stored in session
    # Postcondition: Page with Create Course form is displayed
    # Side Effects: None
    def get(self, request):
        if (request.session["user_id"] == None):
            return render(request, "login.html", {"message": "you do not have access to this page"})

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

        new_user = User(
            user_id=the_id,
            name=request.POST.get('name'),
            password=request.POST.get('password'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
        )

        result_dict = current_user.create_user(new_user)

        return render(request, "create_user.html", {'result': result_dict['result'], 'message': result_dict['message']})

    # this is a dummy method. will eventually use user_id and return a User() class of the user that matches the user_id


def findUser(name):
    # b = User.objects.filter(name=name)
    return User.objects.get(name=name)


# this is a helper method. will eventually use role required & current role to return true if can be accessed, and false if insufficient permissions
def canAccess(role, required_role):
    return True;


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


# helper method to merge dictionaries
def Merge(dict1, dict2):
    dict2.update(dict1)
    return dict2


class Labs(View):
    def get(self, request):
        m = get_user(request.session["user_id"])
        return render(request, "labs.html", {"avaliableTAs": m.avaliableTAs, "avaliableCourses": m.avaliableCourses(),
                                             "avaliableLabs": m.avaliableLabs,
                                             "labAndCourse": m.avaliableLabsandCourses()})

    def post(self, request):
        m = get_user(request.session["user_id"])
        add_to_dict = {"avaliableTAs": m.avaliableTAs, "avaliableCourses": m.avaliableCourses(),
                       "avaliableLabs": m.avaliableLabs}
        if 'ta' in request.POST:
            user_name = request.POST['ta']
            lab_name = request.POST['labs']
            if User.objects.filter(name=user_name).exists() & Lab.objects.filter(lab_name=lab_name).exists():
                user_object = User.objects.get(name=user_name)
                lab_object = Lab.objects.get(lab_name=lab_name)
                return render(request, "labs.html",
                              Merge(add_to_dict, {"message": m.assign_ta_to_lab(user_object,
                                                                                lab_object)}))
            return render(request, "labs.html", Merge(add_to_dict, {"message": "user or lab not found"}))
        else:

            if Course.objects.filter(course_name=request.POST.get('course', False)).exists():
                course = Course.objects.get(course_name=request.POST['course'])
                return render(request, "labs.html",
                              Merge(add_to_dict,
                                    {"message": m.create_lab(request.POST['lab'], request.POST['description'],
                                                             course)}))
            return render(request, "labs.html",
                          Merge(add_to_dict, {"message": "Course not found"}))


class taAssignment(View):

    def get(self, request):
        m = get_user(request.session["user_id"])
        return render(request, "ta_assign.html", {"taAssign": self.getTAassign(m.taAssignments())})

    def getTAassign(self, arr):
        assignments = []
        for val in arr:
            print(val)
            temp = [get_user(val[0]).name, Course.objects.get(course_id=val[1]).course_name, val[2]]
            assignments.append(temp)

        return assignments


class EditUser(View):
    selected = None

    def get(self, request):
        m = get_user(request.session["user_id"])
        return render(request, "edit_user.html", {"editableUsers": m.list_of_editable_users(), "selected": None})

    def post(self, request):
        m = get_user(request.session["user_id"])
        if request.POST.get('reset', False):
            return render(request, "edit_user.html", {"editableUsers": m.list_of_editable_users(), "selected": None})
        if request.POST.get('user-after', False):
            oldUser = User.objects.get(name=request.POST['user-after'])
            message = []
            if request.POST['user_id'] != oldUser.user_id:
                message.append(m.edit_user_id(oldUser, request.POST['user_id']));
            if request.POST['name'] != oldUser.name:
                message.append(m.edit_name(oldUser, request.POST['name']));
            if request.POST['email'] != oldUser.email:
                message.append(m.edit_email(oldUser, request.POST['email']));
            if request.POST['password'] != oldUser.password:
                message.append(m.edit_password(oldUser, request.POST['password']));
            if request.POST['address'] != oldUser.home_address:
                message.append(m.edit_home_address(oldUser, request.POST['address']));
            if request.POST['phone'] != oldUser.phone:
                message.append(m.edit_phone(oldUser, request.POST['phone']));
            if request.POST['role'] != oldUser.role:
                message.append(m.edit_role(oldUser, request.POST['role']));

            return render(request, "edit_user.html", {"editableUsers": m.list_of_editable_users()})


        else:
            return render(request, "edit_user.html", {"editableUsers": m.list_of_editable_users(),
                                                      "selected": User.objects.get(
                                                          name=request.POST.get('user', False))})
