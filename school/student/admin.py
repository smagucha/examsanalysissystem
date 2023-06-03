from django.contrib import admin

from .models import Student, Klass, Stream, Attendance

admin.site.register(Klass)
admin.site.register(Student)
admin.site.register(Stream)
admin.site.register(Attendance)
