from django.contrib import admin
from .models import Student, Klass, Stream, Attendance

admin.site.register(Klass)
admin.site.register(Student)
admin.site.register(Stream)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ["student"]
    list_display = ["student", "class_name", "dateattend", "present_status"]
    list_filter = [
        "student",
        "class_name",
    ]
