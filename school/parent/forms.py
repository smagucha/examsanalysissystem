from .models import Parent
from django.forms import ModelForm
from django import forms


class ParentForm(ModelForm):
    class Meta:
        model = Parent
        fields = "__all__"
