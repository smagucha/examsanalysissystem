from django.shortcuts import render, redirect, get_object_or_404
from .forms import eventsforms
from .models import SchoolEvents
from datetime import date
from django.contrib.auth.decorators import login_required
from student.views import database_operation, delete_database_operation


@login_required(login_url="/accounts/login/")
def addevent(request):
    return database_operation(request, eventsforms)


@login_required(login_url="/accounts/login/")
def listevents(request):
    context_data = {
        "eventlist": SchoolEvents.objects.filter(year=str(date.today().year))
    }
    return render(request, "events/listevents.html", context_data)


@login_required(login_url="/accounts/login/")
def updateevent(request, id):
    return database_operation(request, eventsforms, id)


@login_required(login_url="/accounts/login/")
def delevent(request, id):
    return delete_database_operation(request, SchoolEvents, id)
