from django.contrib import admin

from .models import Teacher, Designation, Teachersubjects

admin.site.register(Teacher)
admin.site.register(Designation)
admin.site.register(Teachersubjects)
