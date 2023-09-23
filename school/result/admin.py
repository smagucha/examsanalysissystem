from django.contrib import admin
from .models import Mark, term, Grading, subject, EnrollStudenttosubect

# Register your models here.

admin.site.register(Grading)
admin.site.register(subject)


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    search_fields = ["marks"]
    list_display = ["student", "name", "marks", "Term"]
    list_filter = ["student__class_name__name", "student__stream__name", "name", "Term"]


@admin.register(term)
class TermAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
    list_filter = ["name"]


@admin.register(EnrollStudenttosubect)
class EnrollStudenttosubectAdmin(admin.ModelAdmin):
    search_fields = ["student", "name"]
    list_display = [
        "student",
        "subject",
    ]
    list_filter = [
        "subject",
        "student__stream__name",
        "student__class_name__name",
    ]
