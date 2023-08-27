from django.urls import path
from . import views

app_name = "parent"
urlpatterns = [
    path("", views.list_parent, name="listparent"),
    path("updateparent/<int:id>/", views.updateparent, name="updateparent"),
    path("deleteparent/<int:id>/", views.deleteparent, name="delparent"),
]
