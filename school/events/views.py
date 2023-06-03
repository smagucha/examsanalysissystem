from django.shortcuts import render, redirect, get_object_or_404
from .forms import eventsforms
from .models import SchoolEvents
from datetime import date
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login/")
def addevent(request):
    if request.method == "POST":
        form = eventsforms(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listevents")
    else:
        form = eventsforms()
    context = {"form": form}
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def listevents(request):
    context = {"eventlist": SchoolEvents.objects.filter(year=str(date.today().year))}
    return render(request, "events/listevents.html", context)


@login_required(login_url="/accounts/login/")
def updateevent(request, id):
    updateid = get_object_or_404(SchoolEvents, id=id)
    if request.method == "POST":
        form = eventsforms(request.POST or None, instance=updateid)
        if form.is_valid():
            form.save()
            return redirect("listevents")
    else:
        form = eventsforms(request.POST or None, instance=updateid)
    context = {
        "title": "update events",
        "updateid": updateid,
        "form": form,
    }
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def delevent(request, id):
    deleteevent = get_object_or_404(SchoolEvents, id=id)
    if request.method == "POST":
        deleteevent.delete()
        return redirect("listevents")
    context = {
        "title": "delete events",
        "deleteevent": deleteevent,
    }
    return render(request, "events/deleteevent.html", context)
