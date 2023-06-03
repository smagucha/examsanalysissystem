from .models import SchoolEvents
from django.forms import ModelForm
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class eventsforms(forms.ModelForm):
    class Meta:
        model = SchoolEvents
        exclude = ["year", "end_of_year"]

        widgets = {"dateevents": DateInput()}
