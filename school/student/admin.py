from django.contrib import admin
from .models import Student, Klass, Stream, Attendance, StudentParent

admin.site.register(Klass)
admin.site.register(Student)
admin.site.register(Stream)
admin.site.register(Attendance)
admin.site.register(StudentParent)
