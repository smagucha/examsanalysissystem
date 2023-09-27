from django.contrib import admin
from django.conf.urls import handler404
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("student.urls")),
    path("teacher/", include("teacher.urls")),
    path("result/", include("result.urls")),
    path("parent/", include("parent.urls")),
    path("events/", include("events.urls")),
    path("useraccounts/", include("useraccounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = "student.views.not_found"
handler400 = "student.views.bad_request"
handler500 = "student.views.server_error"
