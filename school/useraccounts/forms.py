from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyUser
from django.forms import ModelForm


from .models import MyUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "country",
            "date_of_birth",
            "city",
            "phone",
        )


class CustomUserChangeForm(ModelForm):
    class Meta:
        model = MyUser
        fields = (
            "first_name",
            "last_name",
            "country",
            "date_of_birth",
            "city",
            "phone",
        )


class activeform(ModelForm):
    class Meta:
        model = MyUser
        fields = ["first_name", "last_name", "active"]
