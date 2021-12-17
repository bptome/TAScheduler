"""LearnDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from TAInformation.views import Home, Courses, People, DashBoard, Labs,  CreateUser

urlpatterns = [
    path('', Home.as_view()),
    path('courses/', Courses.as_view()),
    path('people/', People.as_view()),
    path('admin/', admin.site.urls),
    path('labs/', Labs.as_view()),
    path('TAInformation/', include('TAInformation.urls')),
    path('create_user/', CreateUser.as_view()),
    # path('addcourse/', AddCourse.as_view()),
    path('dashboard/', DashBoard.as_view()),
]
