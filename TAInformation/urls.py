from django.urls import path

from . import views
from .views import CreateUser

urlpatterns = [
    path('', views.index, name='index'),  # home view
]
