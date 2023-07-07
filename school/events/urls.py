from django.urls import path
from . import views

app_name = "event"
urlpatterns = [
    path("addevent/", views.addevent, name="event"),
    path("", views.listevents, name="listevents"),
    path("updateevent/<int:id>/", views.updateevent, name="updateevent"),
    path("deleteevent/<int:id>/", views.delevent, name="deleteevent"),
]
