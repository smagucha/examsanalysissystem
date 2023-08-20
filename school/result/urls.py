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
        "resultclass/",
        getclasses,
        {"template_name": "result/resultclass.html"},
        name="resultclass",
    ),
    path(
        "classubjectranking/",
        getclasses,
        {"template_name": "result/classsubjectranking.html"},
        name="classubjectranking",
    ),
    path(
        "matokeo/",
        getclasses,
        {"template_name": "result/resultstream.html"},
        name="matokeo",
    ),
    path(
        "subjectrankingclassstream/",
        getclasses,
        {"template_name": "result/subjectrankingclassstream.html"},
        name="subjectrankingclassstream",
    ),
    path(
        "classrankingsubjectterms/<str:classname>/",
        views.terms,
        {"template_name": "result/classrankingsubjectterms.html"},
        name="classrankingsubjectterms",
    ),
    path("deletegrade/<int:id>/", views.deletegrade, name="deletegrade"),
    path("updatesubject/<int:id>/", views.updatesubject, name="updatesubject"),
    path("subjectdelete/<int:id>/", views.subjectdelete, name="subjectdelete"),
    path("Enrollupdate/<int:id>/", views.Enrollupdate, name="Enrollupdate"),
    path("enrolldelete/<int:id>/", views.enrolldelete, name="enrolldelete"),
    path(
        "getstreamsforsubjectranking/<str:name>/",
        getstreams,
        {"template_name": "result/getstreamsforsubjectranking.html"},
        name="getstreamsforsubjectranking",
    ),
    path(
        "k/<str:name>/",
        getstreams,
        {"template_name": "result/streams.html"},
        name="viewstreamresult",
    ),
    path(
        "classterms/<str:classname>/",
        views.terms,
        {"template_name": "result/classresultterm.html"},
        name="classresultterms",
    ),
    path(
        "subjects/<str:classname>/<str:term>/",
        views.getsubjects,
        {"template_name": "result/getsubject.html"},
        name="getallsubjects",
    ),
    path(
        "enterresultclassorstream/<str:classname>/<str:streamname>/",
        views.getsubjects,
        {"template_name": "result/allsubject.html"},
        name="getsubjects",
    ),
    path(
        "enrollclasses/",
        getclasses,
        {"template_name": "result/enrollclasses.html"},
        name="enrollclasses",
    ),
    path(
        "enrollstream/<str:name>/",
        getstreams,
        {"template_name": "result/enrollstream.html"},
        name="enrollstream",
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
        "streamexamanalysis/<str:name>/<str:term>/",
        views.streamexamanalysis,
        {"template_name": "result/performanceterm.html"},
        name="streamexamanalysis",
    ),
    path(
        "enterresults/<str:classname>/<str:streamname>/<str:subject>/",
        views.terms,
        {"template_name": "result/terms.html"},
        name="terms",
    ),
    path(
        "streamresult/<str:classname>/<str:streamname>/",
        views.terms,
        {"template_name": "result/termstreamresult.html"},
        name="termstream",
    ),
    path(
        "subjectperrankclass/<str:name>/<str:term>/<str:subject>/",
        views.subjectperrank,
        {"template_name": "result/analysis.html"},
        name="subjectperrankclass",
    ),
    path(
        "gettermsforsubjectrankstream/<str:classname>/<str:streamname>/",
        views.terms,
        {"template_name": "result/gettermsforsubjectrankstream.html"},
        name="gettermsforsubjectrankstream",
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
        "subjectsrankstream/<str:classname>/<str:streamname>/<str:term>/",
        views.getsubjects,
        {"template_name": "result/getsubjectrankingstream.html"},
        name="getallsubjects",
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
]
