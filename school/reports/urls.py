from django.urls import path
from . import views
app_name = "reports"
urlpatterns = [
    path("<int:id>/<str:name>/", views.report_pdf_view, name="reportcard"),
    path(
        "classanalysis/<str:name>/<str:term>/",
        views.classanalysis,
        name="classanalysis",
    ),
    path(
        "streamanalysis/<str:name>/<str:stream>/<str:term>/",
        views.streamanalysis,
        {'template_name':'reports/streamranalysisdownload.html'},
        name="streamanalysis",
    ),
    path(
        "subjectperrankstreamdownload/<str:name>/<str:stream>/<str:term>/<str:subject>/",
        views.subjectperrankstreamdownload,
        name="subjectperrankstreamdownload",
    ),
    path(
        "subjectperrankclassdownload/<str:name>/<str:term>/<str:subject>/",
        views.subjectperrankclassdownload,
        name="subjectperrankclassdownload",
    ),
    path(
        "export/xls/<str:name>/<str:term>/",
        views.export_users_xls,
        name="export_users_xls",
    ),
   
]
