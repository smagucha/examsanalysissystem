from django.urls import path
from . import views

from student.views import getclasses, getstreams

app_name = "result"
urlpatterns = [
    path("allsubject/", views.allsubject, name="allsubject"),
    path("allGrade/", views.allGrade, name="allGrade"),
    path("allterm/", views.allterm, name="allterm"),
    path("deleteterm/<int:id>/", views.deleteterm, name="deleteterm"),
    path(
        "enrollStudenttosubectall/",
        views.enrollStudenttosubectall,
        name="enrollStudenttosubectall",
    ),
    path("addsubject/", views.addsubject, name="addsubject"),
    path("AddTerm/", views.AddTerm, name="addterm"),
    path("addgrade/", views.addGrade, name="addgrade"),
    path(
        "classubjectranking/",
        views.class_subject_ranking,
        name="classubjectranking",
    ),
    path(
        "matokeo/",
        views.result_stream_or_term,
        name="matokeo",
    ),
    path("deletegrade/<int:id>/", views.deletegrade, name="deletegrade"),
    path("updatesubject/<int:id>/", views.updatesubject, name="updatesubject"),
    path("subjectdelete/<int:id>/", views.subjectdelete, name="subjectdelete"),
    path("Enrollupdate/<int:id>/", views.Enrollupdate, name="Enrollupdate"),
    path("enrolldelete/<int:id>/", views.enrolldelete, name="enrolldelete"),
    path(
        "enrollclasses/",
        views.enroll_students_to_student,
        name="enrollclasses",
    ),
    path(
        "enrollstudentstosubject/<str:name>/<str:stream>/",
        views.enrollstudentstosubject,
        name="enrollstudentstosubject",
    ),
    path(
        "resultperclassterm/<str:name>/<str:term>/",
        views.getresultstreamterm,
        {"template_name": "result/classresultperterm.html"},
        name="resultperterm",
    ),
    path(
        "subjectperfterm/<str:name>/<str:term>/",
        views.streamexamanalysis,
        {"template_name": "result/performanceterm.html"},
        name="subjectperfterm",
    ),
    path(
        "subjectperftermstream/<str:name>/<str:stream>/<str:term>/",
        views.streamexamanalysis,
        {"template_name": "result/performanceterm.html"},
        name="subjectperftermstream",
    ),
    path(
        "enterresults/",
        views.enter_result_for_stream_or_class,
        name="enterresults",
    ),
    path(
        "streamexamanalysis/<str:name>/<str:term>/",
        views.streamexamanalysis,
        {"template_name": "result/performanceterm.html"},
        name="streamexamanalysis",
    ),
    path(
        "subjectperrankclass/<str:name>/<str:term>/<str:subject>/",
        views.subjectperrank,
        {"template_name": "result/analysis.html"},
        name="subjectperrankclass",
    ),
    path(
        "resultstreamterm/<str:name>/<str:stream>/<str:term>/",
        views.getresultstreamterm,
        {"template_name": "result/classresultperterm.html"},
        name="resultstreamterm",
    ),
    path(
        "enterexam/<str:name>/<str:stream>/<str:Term>/<str:Subject>/",
        views.enteresult,
        name="enterexam",
    ),
    path(
        "subjectperrankstreamterm/<str:name>/<str:stream>/<str:term>/<str:subject>/",
        views.subjectperrank,
        {"template_name": "result/analysis.html"},
        name="subjectperrankstreamterm",
    ),
    path(
        "student-detail/<str:name>/<int:id>/", views.student_view, name="student-detail"
    ),
    # new pdf paths
    path(
        "streamanalysis/<str:name>/<str:stream>/<str:term>/",
        views.streamexamanalysis,
        {"template_name": "result/streamranalysisdownload.html", "format": "pdf"},
        name="streamanalysispdf",
    ),
    path(
        "streamanalysis/<str:name>/<str:term>/",
        views.streamexamanalysis,
        {"template_name": "result/streamranalysisdownload.html", "format": "pdf"},
        name="streamanalysispdf",
    ),
    path(
        "subjectperrankstreamterm/<str:name>/<str:stream>/<str:term>/<str:subject>/pdf/",
        views.subjectperrank,
        {"template_name": "result/subjectperrankclassdownload.html", "format": "pdf"},
        name="subjectperrankstreamtermpdf",
    ),
    path(
        "subjectperrankclasspdf/<str:name>/<str:term>/<str:subject>/pdf/",
        views.subjectperrank,
        {"template_name": "result/subjectperrankclassdownload.html", "format": "pdf"},
        name="subjectperrankclasspdf",
    ),
    path(
        "reportcard/<str:name>/<int:id>/<str:termname>/",
        views.reportbook,
        name="reportcard",
    ),
    # links for excels
    path(
        "downresultexcel/<str:name>/<str:term>/",
        views.getresultstreamterm,
        {"format": "ms-excel"},
        name="resultpertermexcel",
    ),
    path(
        "downresultexcel/<str:name>/<str:stream>/<str:term>/",
        views.getresultstreamterm,
        {"format": "ms-excel"},
        name="resultpertermexcelstream",
    ),
    path(
        "studentenrolledsubjects/",
        views.subjects_enrolled_y_student,
        name="studentenrolledsubjects",
    ),
    path(
        "update_subjects_enrolled_y_student/<int:id>/",
        views.update_subjects_enrolled_y_student,
        name="update_subjects_enrolled_y_student",
    ),
    path(
        "delete_subjects_enrolled_y_student/<int:id>/",
        views.update_subjects_enrolled_y_student,
        name="delete_subjects_enrolled_y_student",
    ),
    path("classstreamraking", views.class_and_stream_ranking, name="classstreamraking"),
]
