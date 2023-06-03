from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("student.urls")),
    path("teacher/", include("teacher.urls")),
    path("result/", include("result.urls")),
    path("parent/", include("parent.urls")),
    path("events/", include("events.urls")),
    path("useraccounts/", include("useraccounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
