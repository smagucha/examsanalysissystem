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
    # path("getclasses/", views.getclasses, name="enterresulturl"),
    path(
        "takeattendance/",
        views.take_attendance,
        name="takeattendance",
    ),
    path("deleteattend/<int:id>/", views.deleteattend, name="deleteattend"),
    path("schoolsetting/", views.schoolsetting, name="schoolsetting"),
    path("addclasses/", views.addclasses, name="addclasses"),
    path("addstreams/", views.addstreams, name="addstreams"),
    path(
        "allclasses/",
        views.getclasses,
        {"template_name": "student/classes.html"},
        name="allclasses",
    ),
    path(
        "stream/",
        views.getstreams,
        {"template_name": "student/stream.html"},
        name="stream",
    ),
    path("objectnotfound/", views.objectnotfound, name="objectnotfound"),
    path("deletestudent/<int:id>/", views.delete_student, name="delete_student"),
    path("viewattendance/", views.viewattendance, name="viewattendance"),
]
