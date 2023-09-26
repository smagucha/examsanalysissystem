from django.forms import ModelForm
from .models import Student, Attendance, Klass, Stream
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            "date_of_birth": DateInput(),
            "date_of_admission": DateInput(),
        }


class AttendForm(ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"


class KlassForm(ModelForm):
    class Meta:
        model = Klass
        fields = "__all__"


class StreamForm(ModelForm):
    class Meta:
        model = Stream
        fields = "__all__"
