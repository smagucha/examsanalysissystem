from django.urls import path
from . import views

urlpatterns = [
    path("parentsignup/", views.parentsignup, name="signup"),
    path("teachersignup/", views.teachersignup, name="teachersignup"),
    path("updateprofile/", views.updateprofile, name="updateprofile"),
    path("activateuser/<int:id>/", views.activateuser, name="activateuser"),
    path("alluser/", views.alluser, name="alluser"),
]
