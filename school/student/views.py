from django.shortcuts import render, redirect
from .models import Student, Klass, Attendance, Stream
from .forms import StudentForm, AttendForm, KlassForm, StreamForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


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
    if stream:
        students = Student.student.get_student_list_stream(name=name, stream=stream)
    else:
        students = Student.student.get_student_list_class(name=name)
    if stream:
        context = {
            "title": "class students",
            "student": students,
        }
    else:
        context = {
            "title": "class students",
            "student": students,
            "name": name,
            "allstream": Stream.objects.all(),
        }
    return render(request, template_name, context)


@login_required(login_url="/accounts/login/")
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("student:home")
    else:
        form = StudentForm()
    context = {"title": "add student", "form": form}
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def update_student(request, id):
    student = Student.objects.get(id=id)
    if request.method == "POST":
        form = StudentForm(request.POST or None, instance=student)
        if form.is_valid:
            form.save()
            return redirect("home")
    else:
        form = StudentForm(instance=student)
    context = {"title": "add student", "form": form}
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def delete_student(request, id):
    student = Student.objects.get(id=id)
    try:
        student.delete()
    except ObjectDoesNotExist:
        return redirect("home")


@login_required(login_url="/accounts/login/")
def Take_Attandance(request, name, stream):
    takeattendance = Student.student.get_student_list_stream(name=name, stream=stream)
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
    attend = Attendance.objects.get(id=id)
    if request.method == "POST":
        form = AttendForm(request.POST or None, instance=attend)
        if form.is_valid:
            form.save()
            return redirect("home")
    else:
        form = AttendForm(instance=attend)
    context = {"title": "view attendance", "form": form}
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def deleteattend(request, id):
    attend = Attendance.objects.get(id=id)
    try:
        attend.delete()
    except ObjectDoesNotExist:
        return redirect("home")


@login_required(login_url="accounts/login/")
def schoolsetting(request):
    return render(request, "student/schoolsetting.html")


@login_required(login_url="accounts/login/")
def addclasses(request):
    if request.method == "POST":
        form = KlassForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("student:home")
    else:
        form = KlassForm()
    context = {"title": "add classes", "form": form}
    return render(request, "student/generalform.html", context)


@login_required(login_url="accounts/login")
def addstreams(request):
    if request.method == "POST":
        form = StreamForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("student:home")
    else:
        form = StreamForm()
    context = {"title": "add classes", "form": form}
    return render(request, "student/generalform.html", context)


def not_found(request, exception):
    return render(request, "student/404.html")


def server_error(request, exception=None):
    return render(request, "student/500.html")


def bad_request(request, exception):
    return render(request, "student/400.html")
