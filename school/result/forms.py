from .models import subject, term, Grading, EnrollStudenttosubect, Mark
from django.forms import ModelForm


class subjectForm(ModelForm):
    class Meta:
        model = subject
        fields = "__all__"


class TermForm(ModelForm):
    class Meta:
        model = term
        fields = "__all__"


class GradeForm(ModelForm):
    class Meta:
        model = Grading
        fields = "__all__"


class EnrollForm(ModelForm):
    class Meta:
        model = EnrollStudenttosubect
        exclude = ["year", "end_of_year"]


class MarkForm(ModelForm):
    class Meta:
        model = Mark
        fields = "__all__"
