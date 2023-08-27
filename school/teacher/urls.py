from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_Teacher, name="listTeacher"),
    path("updateTeacher/<int:id>/", views.updateTeacher, name="updateTeacher"),
    path("deleteTeacher/<int:id>/", views.deleteTeacher, name="deleteTeacher"),
    path("addteacher/", views.addTeacher, name="addTeacher"),
    path("adddesignation/", views.adddesignation, name="adddesignation"),
    path("alldesignation/", views.alldesignation, name="alldesignation"),
    path(
        "updatedesignation/<int:id>/", views.updatedesignation, name="updatedesignation"
    ),
    path(
        "deletedesignation/<int:id>/", views.deletedesignation, name="deletedesignation"
    ),
    path("addTeachersubjects/", views.addTeachersubjects, name="addTeachersubjects"),
    path(
        "list_Teacher_subjects/",
        views.list_Teacher_subjects,
        name="listTeachersubjects",
    ),
    path("updateteachersub/<int:id>/", views.updateteachersub, name="updateteachersub"),
    path("deleteteachersub/<int:id>/", views.deleteteachersub, name="deleteteachersub"),
    path("teacher_view/", views.teacher_view, name="teacherview"),
]
