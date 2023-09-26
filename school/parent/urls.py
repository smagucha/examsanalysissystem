from django.urls import path
from . import views

app_name = "parent"
urlpatterns = [path("", views.list_parent, name="listparent")]
