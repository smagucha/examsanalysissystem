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
        "Take_Attandance/<str:name>/",
        views.Take_Attandance,
        name="takeattandanceclass",
    ),
    path(
        "viewattendanceperstream/<str:name>/<str:stream>/",
        views.viewattendanceperstream,
        name="viewattendanceperstream",
    ),
    path(
        "viewattendanceperclass/<str:name>/",
        views.viewattendanceperstream,
        name="viewattendanceperclass",
    ),
    path("attendupdate/<int:id>/", views.attendupdate, name="updateattend"),
    path(
        "takeattendance/",
        views.take_attendance,
        name="takeattendance",
    ),
    path("deleteattend/<int:id>/", views.deleteattend, name="deleteattend"),
    path("schoolsetting/", views.schoolsetting, name="schoolsetting"),
    path("addclasses/", views.addclasses, name="addclasses"),
    path("updateclass/<int:id>/", views.updateclass, name="updateclass"),
    path("deleteclass/<int:id>/", views.deleteclass, name="deleteclass"),
    path("allclasses", views.allclasses, name="allclasses"),
    path("addstreams/", views.addstreams, name="addstreams"),
    path("allstreams", views.allstreams, name="allstreams"),
    path("updatestream/<int:id>/", views.updatestream, name="updatestream"),
    path("deletestream/<int:id>/", views.deletestream, name="deletestream"),
    path("objectnotfound/", views.objectnotfound, name="objectnotfound"),
    path("deletestudent/<int:id>/", views.delete_student, name="delete_student"),
    path("viewattendance/", views.viewattendance, name="viewattendance"),
]
