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


def Course(View):
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
