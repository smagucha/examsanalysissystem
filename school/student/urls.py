from django.urls import path
from . import views

app_name = "student"
urlpatterns = [
    path("", views.student_list, name="home"),
    path(
        "class/<str:name>/",
        views.student_class,
        {"template_name": "student/student_list.html"},
        name="classstudent",
    ),
    path(
        "class/<str:name>/<str:stream>/",
        views.student_class,
        {"template_name": "student/student_list.html"},
        name="streamstudent",
    ),
    path("addstudent/", views.add_student, name="addstudent"),
    path("update_student/<int:id>/", views.update_student, name="updatestudent"),
    path(
        "Take_Attandance/<str:name>/<str:stream>/",
        views.Take_Attandance,
        name="takeattandance",
    ),
    path(
        "viewattendanceperstream/<str:name>/<str:stream>/",
        views.viewattendanceperstream,
        name="viewattendanceperstream",
    ),
    path("attendupdate/<int:id>/", views.attendupdate, name="updateattend"),
    path("getclasses/", views.getclasses, name="enterresulturl"),
    path(
        "takeattendance/",
        views.getclasses,
        {"template_name": "student/classattend.html"},
        name="takeattendance",
    ),
    path(
        "<str:name>/takeattendancestream/",
        views.getstreams,
        {"template_name": "student/attendancestreams.html"},
        name="takeattendancestream",
    ),
    path(
        "viewattendance/",
        views.getclasses,
        {"template_name": "student/viewattendclasses.html"},
        name="viewattendance",
    ),
    path(
        "<str:name>/viewattendancestream/",
        views.getstreams,
        {"template_name": "student/viewattendancestream.html"},
        name="viewattendancestream",
    ),
    path(
        "enterresults/",
        views.getclasses,
        {"template_name": "student/enterresultsclass.html"},
        name="enterresults",
    ),
    path(
        "<str:name>/choicetoenterstreamresult/",
        views.getstreams,
        {"template_name": "student/enterstreamresult.html"},
        name="enterstreamresult",
    ),
]
