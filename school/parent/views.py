from django.shortcuts import render, get_object_or_404, redirect
from .forms import ParentForm
from .models import Parent
from student.models import Student
from datetime import date
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login/")
def list_parent(request):
    # parents = Parent.objects.filter(student__year=str(date.today().year)).distinct()
    parents = Parent.objects.all()
    context = {
        "title": "all parents",
        "getParents": parents,
    }
    return render(request, "parent/parent.html", context)


@login_required(login_url="/accounts/login/")
def updateparent(request, id):
    idparent = get_object_or_404(Parent, id=id)
    if request.method == "POST":
        form = ParentForm(request.POST or None, request.FILES, instance=idparent)
        if form.is_valid():
            form.save()
            return redirect("parent:listparent")
    else:
        form = ParentForm(request.POST or None, instance=idparent)
    context = {
        "title": "update parent",
        "idparent": idparent,
        "form": form,
    }
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def deleteparent(request, id):
    delparent = get_object_or_404(Parent, id=id)
    if request.method == "POST":
        delparent.delete()
        redirect("parent:listparent")
    context = {
        "title": "remove parent",
        "delparent": delparent,
    }
    return render(request, "parent/deleteparent.html", context)


@login_required(login_url="/accounts/login/")
def addparent(request):
    if request.method == "POST":
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("parent:listparent")
    else:
        form = ParentForm()
    context = {
        "title": "add parent",
        "form": form,
    }
    return render(request, "student/generalform.html", context)
