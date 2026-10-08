from django.contrib import admin
from .models import UserProfile, Classroom, Assignment, Submission

admin.site.register(UserProfile)
admin.site.register(Classroom)
admin.site.register(Assignment)
admin.site.register(Submission)