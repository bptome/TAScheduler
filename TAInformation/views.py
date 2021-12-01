from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views import View


def index(request):
    return HttpResponse("Hello , world. You're at the polls index.")


class Home(View):
    def get(self, request):
        return render(request, "login.html", {})
