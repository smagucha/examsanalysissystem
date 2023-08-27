from django.shortcuts import render, get_object_or_404, redirect
from .forms import TeacherForm, DesignationForm, TeachersubjectForm
from .models import Teacher, Designation, Teachersubjects
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from student.views import database_operation, delete_database_operation
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login/")
def list_Teacher(request):
    listTeacher = Teacher.objects.all()
    context = {
        "title": "all Teachers",
        "listTeacher": listTeacher,
    }
    return render(request, "teacher/allTeachers.html", context)


@login_required(login_url="/accounts/login/")
def updateTeacher(request, id):
    return database_operation(request, TeacherForm, id)


@login_required(login_url="/accounts/login/")
def deleteTeacher(request, id):
    return delete_database_operation(request, Teacher, id)


@login_required(login_url="/accounts/login/")
def addTeacher(request):
    return database_operation(request, TeacherForm)


@login_required(login_url="/accounts/login/")
def adddesignation(request):
    return database_operation(request, DesignationForm)


@login_required(login_url="/accounts/login/")
def alldesignation(request):
    return render(
        request,
        "teacher/alldesignation.html",
        context={
            "alldesignation": Designation.objects.all(),
        },
    )


@login_required(login_url="/accounts/login/")
def updatedesignation(request, id):
    return database_operation(request, DesignationForm, id)


@login_required(login_url="/accounts/login/")
def deletedesignation(request, id):
    return delete_database_operation(request, Designation, id)


@login_required(login_url="/accounts/login/")
def addTeachersubjects(request):
    return database_operation(request, TeachersubjectForm)


@login_required(login_url="/accounts/login/")
def list_Teacher_subjects(request):
    return render(
        request,
        "teacher/list_Teacher_subjects.html",
        context={
            "allsubjectataught": Teachersubjects.objects.all(),
        },
    )


@login_required(login_url="/accounts/login/")
def updateteachersub(request, id):
    return database_operation(request, TeachersubjectForm, id)


@login_required(login_url="/accounts/login/")
def deleteteachersub(request, id):
    return delete_database_operation(request, Teachersubjects, id)


@login_required(login_url="/accounts/login/")
def teacher_view(request):
    return render(request, "teacher/teacherview.html")
