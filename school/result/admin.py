from django.contrib import admin
from .models import Mark, term, Grading, subject, EnrollStudenttosubect

# Register your models here.

admin.site.register(Grading)
admin.site.register(subject)


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    search_fields = ["marks"]
    list_display = ["student", "name", "marks", "Term"]
    list_filter = ["student", "name", "marks", "Term"]


@admin.register(term)
class TermAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
    list_filter = ["name"]


@admin.register(EnrollStudenttosubect)
class EnrollStudenttosubectAdmin(admin.ModelAdmin):
    # search_fields = ['student']
    # list_display = ['student' ]
    list_filter = ["subject"]
