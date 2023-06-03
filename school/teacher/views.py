from django.shortcuts import render, get_object_or_404, redirect
from .forms import TeacherForm, DesignationForm  # , TeachersubjectForm
from .models import Teacher, Designation  # , Teachersubjects
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group


def list_Teacher(request):
    listTeacher = Teacher.objects.all()
    context = {
        "title": "all Teachers",
        "listTeacher": listTeacher,
    }
    return render(request, "teacher/allTeachers.html", context)


def updateTeacher(request, id):
    idTeacher = get_object_or_404(Teacher, id=id)
    if request.method == "POST":
        form = TeacherForm(request.POST or None, request.FILES, instance=idTeacher)
        if form.is_valid():
            form.save()
            return redirect("listTeacher")
    else:
        form = TeacherForm(request.POST or None, instance=idTeacher)
    context = {
        "title": "update Teacher",
        "idTeacher": idTeacher,
        "form": form,
    }
    return render(request, "student/generalform.html", context)


def deleteTeacher(request, id):
    delTeacher = get_object_or_404(Teacher, id=id)
    if request.method == "POST":
        delTeacher.delete()
        redirect("listTeacher")
    context = {
        "title": "remove Teacher",
        "delTeacher": delTeacher,
    }
    return render(request, "teacher/deleteTeacher.html", context)


def addTeacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("listTeacher")
    else:
        form = TeacherForm()
    context = {
        "title": "add Teacher",
        "form": form,
    }
    return render(request, "student/generalform.html", context)


def adddesignation(request):
    if request.method == "POST":
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            form = DesignationForm()
            return redirect("home")
    else:
        form = DesignationForm()
    context = {"title": "add designation", "form": form}
    return render(request, "student/generalform.html", context)


def alldesignation(request):
    return render(
        request,
        "teacher/alldesignation.html",
        context={
            "alldesignation": Designation.objects.all(),
        },
    )


def updatedesignation(request, id):
    getdesign = get_object_or_404(Designation, id=id)
    form = DesignationForm()
    if request.method == "POST":
        form = DesignationForm(request.POST or None, instance=getdesign)
        if form.is_valid:
            form.save()
            return redirect("alldesignation")
    else:
        form = DesignationForm(instance=getdesign)
    context = {
        "form": form,
    }
    return render(request, "student/generalform.html", context)


def deletedesignation(request, id):
    getdesign = get_object_or_404(Designation, id=id)
    if request.method == "POST":
        getdesign.delete()
        return redirect("alldesignation")
    context = {
        "title": "delete designation",
    }
    return render(request, "teacher/deletedesignation.html", context)


def addTeachersubjects(request):
    form = TeachersubjectForm()
    if request.method == "POST":
        form = TeachersubjectForm(request.POST)
        if form.is_valid():
            form.save()
            form = TeachersubjectForm()
    else:
        form = TeachersubjectForm()
    context = {
        "form": form,
    }
    return render(request, "student/generalform.html", context)


def list_Teacher_subjects(request):
    return render(
        request,
        "teacher/list_Teacher_subjects.html",
        context={
            "allsubjectataught": Teachersubjects.objects.all(),
        },
    )


def updateteachersub(request, id):
    updatesubject = get_object_or_404(Teachersubjects, id=id)
    form = TeachersubjectForm()
    if request.method == "POST":
        form = TeachersubjectForm(request.POST or None, instance=updatesubject)
        if form.is_valid():
            form.save()
            return redirect("list_Teacher_subjects")
    else:
        form = TeachersubjectForm(instance=updatesubject)

    context = {"form": form, "updatesubject": updatesubject}

    return render(request, "student/generalform.html", context)


def deleteteachersub(request, id):
    delsubject = get_object_or_404(Teachersubjects, id=id)
    if request.method == "POST":
        delsubject.delete()
    context = {"delsubject": delsubject}
    return render(request, "teacher/deleteteachersub.html", context)
