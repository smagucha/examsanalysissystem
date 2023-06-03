from .models import Teacher, Designation, Teachersubjects
from django import forms
from django.forms import ModelForm


class DateInput(forms.DateInput):
    input_type = "date"


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"
        widgets = {
            "date_of_appointment": DateInput(),
        }


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = "__all__"


class TeachersubjectForm(forms.ModelForm):
    class Meta:
        model = Teachersubjects
        fields = "__all__"
