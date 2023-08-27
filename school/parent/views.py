from django.shortcuts import render, get_object_or_404, redirect
from student.forms import StudentParentForm
from .models import Parent
from student.models import Student, StudentParent
from datetime import date
from django.contrib.auth.decorators import login_required
from student.views import database_operation, delete_database_operation


@login_required(login_url="/accounts/login/")
def list_parent(request):
    parents_with_students = StudentParent.objects.filter(
        student__year=date.today().year
    )
    context = {
        "title": "all parents",
        "getParents": parents_with_students,
    }
    return render(request, "parent/parent.html", context)


@login_required(login_url="/accounts/login/")
def updateparent(request, id):
    return database_operation(request, StudentParentForm, id)


@login_required(login_url="/accounts/login/")
def deleteparent(request, id):
    return delete_database_operation(request, StudentParentForm, id)
