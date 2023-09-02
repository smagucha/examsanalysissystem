from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Klass, Attendance, Stream
from .forms import StudentForm, AttendForm, KlassForm, StreamForm, StudentParentForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from result.models import term


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


# # # delete this function after through testing
@login_required(login_url="/accounts/login/")
def getclasses(request, template_name):
    getallclasses = Klass.objects.all()
    context = {"allclasses": getallclasses}
    return render(request, template_name, context)


# delete this function after through testing
@login_required(login_url="/accounts/login/")
def getstreams(request, template_name, name=None):
    getstream = Stream.objects.all()
    context = {"allstream": getstream, "name": name}
    return render(request, template_name, context)


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
        getclass = Klass.objects.get(name=name)
        x = [student.id for student in takeattendance]
        result.append(x)
        result.append(getclass.id)
        result.append(getreason)
        result.append(getpresent)
        if stream:
            getstream = Stream.objects.get(name=stream)
            result.append(getstream.id)

        for j in range(len(result[0])):
            attendance_data = {
                "class_name_id": result[1],
                "student_id": result[0][j],
                "present_status": result[3][j],
                "absentwhy": result[2][j],
            }
            if stream:
                attendance_data["stream_id"] = result[4]

            attend = Attendance.objects.create(**attendance_data)
            attend.save()

        if stream:
            return redirect("student:viewattendanceperstream", name=name, stream=stream)
        else:
            return redirect("student:viewattendance", name=name)

    context = {"exam": takeattendance}
    return render(request, "student/attend.html", context)


# modify this function to fit if there is no stream (for class only)
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


# this changes everything for code
# works as expects
@login_required(login_url="/accounts/login/")
def viewattendance(request):
    if request.method == "POST":
        selected_class = request.POST.get("selected_class")
        selected_stream = request.POST.get("selected_stream")
        return redirect(
            "student:viewattendanceperstream",
            name=selected_class,
            stream=selected_stream,
        )
    context = {"getclasses": Klass.objects.all(), "getstream": Stream.objects.all()}
    return render(request, "student/takeviewattendance.html", context)


def get_class():
    return Klass.objects.all()


def get_stream():
    return Stream.objects.all()


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


@login_required(login_url="/accounts/login/")
def add_student_to_parent(request):
    return database_operation(request, StudentParentForm)
