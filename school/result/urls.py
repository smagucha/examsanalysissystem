from django.urls import path
from . import views

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
        "enterexamforclass/<str:name>/<str:Term>/<str:Subject>/",
        views.enteresult,
        name="enterexamforclass",
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
        "select_class_subject_enrolled",
        views.select_class_subject_enrolled,
        name="select_class_subject_enrolled",
    ),
    path(
        "studentenrolledsubjects/<str:name>/<str:stream>/<str:subject>/",
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
    path(
        "classstreamraking/", views.class_and_stream_ranking, name="classstreamraking"
    ),
    path("select_class/", views.select_class_for_stream_ranking, name="selectclass"),
    path(
        "streamranking/<str:name>/<str:term>/",
        views.stream_ranking,
        name="streamranking",
    ),
    path("classranking/<str:term>/", views.calculate_class_ranks, name="classranking"),
    path(
        "select_stream_for_subject_ranking/",
        views.select_stream_for_subject_ranking,
        name="streamsubjecranking",
    ),
    path(
        "subjectrankingstream/<str:class_name>/<str:term>/<str:subject>/",
        views.class_stream_subject_ranking,
        name="subjectrankingstream",
    ),
    path(
        "termclassranking/",
        views.select_term_for_class_ranking,
        name="termclassranking",
    ),
    path(
        "subject_results_class/<str:class_name>/<str:term>/<str:subject>/<str:stream>/",
        views.subject_results_class,
        name="sujectresults",
    ),
    path(
        "subject_results_class/<str:class_name>/<str:term>/<str:subject>",
        views.subject_results_class,
        name="sujectresultsclass",
    ),
    path("updateresult/<int:id>/", views.updatemarks, name="updatemarks"),
    path(
        "select_class_to_sent_result/",
        views.select_class_to_sent_result,
        name="selectclasstosentresult",
    ),
    path(
        "select_result_to_update/", views.select_result_to_update, name="selectupdate"
    ),
    path(
        "sent_results/<str:class_name>/<str:term>/",
        views.sent_results,
        name="sentresultspage",
    ),
    path("send_sms_view/", views.send_sms_view, name="messagesuccess"),
]
