from django.forms import ModelForm
from .models import Student, Attendance


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class AttendForm(ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"
