from django.contrib import admin

# Register your models here.

from .models import CourseTAJunction, User

admin.site.register(CourseTAJunction)
admin.site.register(User)
