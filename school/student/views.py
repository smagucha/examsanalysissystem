from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Klass, Attendance, Stream
from .forms import StudentForm, AttendForm, KlassForm, StreamForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


@login_required(login_url="/accounts/login/")
def database_operation(request, form_class, id=None):
    if id:
        instance = get_object_or_404(form_class.Meta.model, id=id)
    else:
        instance = None

    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            form = form_class()
    else:
        form = form_class(instance=instance)

    if id:
        title = "Update Data"
    else:
        title = "Add Data"
    context = {"form": form, "title": title}
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def delete_database_operation(request, mymodel, id):
    try:
        instance = get_object_or_404(mymodel, id=id).delete()
    except:
        return redirect("student:objectnotfound")
    return render(request, "student/delete.html")


@login_required(login_url="/accounts/login/")
def getclasses(request, template_name):
    getallclasses = Klass.objects.all()
    context = {"allclasses": getallclasses}
    return render(request, template_name, context)


@login_required(login_url="/accounts/login/")
def getstreams(request, template_name, name=None):
    getstream = Stream.objects.all()
    context = {"allstream": getstream, "name": name}
    return render(request, template_name, context)


@login_required(login_url="/accounts/login/")
def student_list(request):
    students = Student.student.get_student_list()
    allclasses = Klass.objects.all()
    context = {"title": "all students", "student": students, "allclasses": allclasses}
    return render(request, "student/student_list.html", context)


@login_required(login_url="/accounts/login/")
def student_class(request, name, stream=None, template_name=None):
    students = Student.student.get_student_list_class_or_stream(
        name=name, stream=stream
    )
    context = {
        "title": "class students",
        "student": students,
    }
    if name:
        context["name"] = name
        context["allstream"] = Stream.objects.all()
    return render(request, template_name, context)


@login_required(login_url="/accounts/login/")
def add_student(request):
    return database_operation(request, StudentForm)


@login_required(login_url="/accounts/login/")
def update_student(request, id):
    return database_operation(request, StudentForm, id)


@login_required(login_url="/accounts/login/")
def delete_student(request, id):
    return delete_database_operation(request, Student, id)


@login_required(login_url="/accounts/login/")
def Take_Attandance(request, name, stream):
    takeattendance = Student.student.get_student_list_class_or_stream(name, stream)
    result = []
    if request.method == "POST":
        getreason = request.POST.getlist(
            "reason",
        )
        getpresent = request.POST.getlist("present_status")
        getclass = Klass.objects.get(name=name)
        getstream = Stream.objects.get(name=stream)
        x = []
        for i in takeattendance:
            x.append(i.id)
        result.append(x)
        result.append(getclass.id)
        result.append(getreason)
        result.append(getpresent)
        result.append(getstream.id)
        for j in range(len(result[0])):
            attend = Attendance.objects.create(
                class_name_id=result[1],
                student_id=result[0][j],
                present_status=result[3][j],
                absentwhy=result[2][j],
                stream_id=result[4],
            )
            attend.save()
        return redirect("student:viewattendanceperstream", name=name, stream=stream)

    context = {"exam": takeattendance}
    return render(request, "student/attend.html", context)


@login_required(login_url="/accounts/login/")
def viewattendanceperstream(request, name, stream):
    attend = Attendance.attend.get_student_list_stream(name=name, stream=stream)
    context = {"title": "view attendance", "attend": attend}
    return render(request, "student/viewattend.html", context)


@login_required(login_url="/accounts/login/")
def attendupdate(request, id):
    return database_operation(request, AttendForm, id)


@login_required(login_url="/accounts/login/")
def deleteattend(request, id):
    return delete_database_operation(request, Attendance, id)


@login_required(login_url="accounts/login/")
def schoolsetting(request):
    return render(request, "student/schoolsetting.html")


@login_required(login_url="/accounts/login/")
def addclasses(request):
    return database_operation(request, KlassForm, id=None)


@login_required(login_url="/accounts/login/")
def addstreams(request):
    return database_operation(request, StreamForm, id=None)


def not_found(request, exception):
    return render(request, "student/404.html")


def server_error(request, exception=None):
    return render(request, "student/500.html")


def bad_request(request, exception):
    return render(request, "student/400.html")


@login_required(login_url="/accounts/login/")
def objectnotfound(request):
    return render(request, "student/objectnotfound.html")
