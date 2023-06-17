from django.forms import ModelForm
from .models import Student, Attendance, Klass, Stream


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


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
