from django.contrib import admin
from .models import UserProfile, Classroom, Assignment

admin.site.register(UserProfile)
admin.site.register(Classroom)
admin.site.register(Assignment)