from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, activeform
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from useraccounts.models import MyUser


def parentsignup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data["email"]
            user = MyUser.objects.get(email=email)
            # group = Group.objects.get(name="Parent")
            # user.groups.add(group)
            user.save()
            return redirect("student:home")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "useraccounts/sign_up.html", context)


def teachersignup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            user = User.objects.get(username=username)
            # group = Group.objects.get(name="Teacher")
            # user.groups.add(group)
            user.save()
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "useraccounts/sign_up.html", context)


@login_required(login_url="/accounts/login/")
def updateprofile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("student:home")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "student/forms.html", context)


def activateuser(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = activeform(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("alluser")
    else:
        form = activeform(instance=user)

    context = {"form": form, "user": user}
    return render(request, "useraccounts/activateuser.html", context)
