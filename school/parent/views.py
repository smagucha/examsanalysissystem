from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student.models import Student


@login_required(login_url="/accounts/login/")
def list_parent(request):
    parents_with_students = Student.student.get_student_list()
    context = {
        "title": "all parents",
        "getParents": parents_with_students,
    }
    return render(request, "parent/parent.html", context)
