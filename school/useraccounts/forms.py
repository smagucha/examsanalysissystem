from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class userupdateform(ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class activeform(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "is_active"]
