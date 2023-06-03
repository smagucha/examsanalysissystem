from django.shortcuts import render, redirect
from .forms import SignUpForm, activeform
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import userupdateform
from django.contrib.auth.models import Group, User, Permission


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            user = User.objects.get(username=username)
            group = Group.objects.get(name="Parent")
            user.is_active = False
            user.groups.add(group)
            user.save()
            return redirect("home")
    else:
        form = SignUpForm()
    context = {"form": form}
    return render(request, "useraccounts/sign_up.html", context)


def teachersignup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            user = User.objects.get(username=username)
            group = Group.objects.get(name="Teacher")
            user.is_active = False
            user.groups.add(group)
            user.save()
            return redirect("home")
    else:
        form = SignUpForm()
    context = {"form": form}
    return render(request, "useraccounts/sign_up.html", context)


@login_required(login_url="/accounts/login/")
def updateprofile(request):

    if request.method == "POST":
        form = userupdateform(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("alluser")
    else:
        form = userupdateform(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "useraccounts/edit_profile.html", context)


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
