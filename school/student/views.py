from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Klass, Attendance, Stream
from .forms import StudentForm, AttendForm, KlassForm, StreamForm
from django.contrib.auth.decorators import login_required
from .utils import get_class, get_stream
from datetime import datetime


@login_required(login_url="/accounts/login/")
def database_operation(request, form_class, id=None):
    if id:
        instance = get_object_or_404(form_class.Meta.model, id=id)
    else:
        instance = None

    form = form_class(request.POST or None, instance=instance)

    if request.method == "POST" and form.is_valid():
        form.save()
        redirect_url = request.POST.get("next", "student:home")
        return redirect(redirect_url)

    context = {"form": form, "title": "Update Data" if id else "Add Data"}
    return render(request, "student/generalform.html", context)


@login_required(login_url="/accounts/login/")
def delete_database_operation(request, mymodel, id):
    try:
        instance = get_object_or_404(mymodel, id=id).delete()
        return redirect("student:home")
    except:
        return redirect("student:objectnotfound")
    return render(request, "student/delete.html")


@login_required(login_url="/accounts/login/")
def student_list(request):
    student_count = Student.student.get_total_students()
    allclasses = Klass.objects.all()
    context = {
        "title": "all students",
        "allclasses": allclasses,
        "student_count": student_count,
    }
    return render(request, "student/studenthome.html", context)


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
def Take_Attandance(request, name, stream=None):
    takeattendance = Student.student.get_student_list_class_or_stream(name, stream)
    result = []
    if request.method == "POST":
        getreason = request.POST.getlist("reason")
        getpresent = request.POST.getlist("present_status")
        for i, student in enumerate(takeattendance):
            attendance_data = {
                "class_name_id": student.class_name.id,
                "student_id": student.id,
                "present_status": getpresent[i],
                "absentwhy": getreason[i],
                "stream": student.stream,
            }
            attend = Attendance.objects.create(**attendance_data)
            attend.save()
        return redirect("student:viewattendanceperstream", name=name, stream=stream)
    context = {"exam": takeattendance}
    return render(request, "student/attend.html", context)


@login_required(login_url="/accounts/login/")
def viewattendanceperstream(request, name, stream=None):
    current_month = datetime.now().month
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


@login_required(login_url="/accounts/login/")
def viewattendance(request):
    if request.method == "POST":
        selected_class = request.POST.get("selected_class")
        selected_stream = request.POST.get("selected_stream")
        if selected_stream:
            return redirect(
                "student:viewattendanceperstream",
                name=selected_class,
                stream=selected_stream,
            )
        else:
            return redirect("student:viewattendanceperclass", name=selected_class)
    context = {"getclasses": Klass.objects.all(), "getstream": Stream.objects.all()}
    return render(request, "student/takeviewattendance.html", context)


@login_required(login_url="/accounts/login/")
def take_attendance(request):
    if request.method == "POST":
        selected_class = request.POST.get("selected_class")
        selected_stream = request.POST.get("selected_stream")
        if selected_stream:
            return redirect(
                "student:takeattandance",
                name=selected_class,
                stream=selected_stream,
            )
        else:
            return redirect("student:takeattandanceclass", name=selected_class)

    context = {"getclasses": get_class(), "getstream": get_stream()}
    return render(request, "student/takeviewattendance.html", context)
