from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("<str:username>", views.lobby, name="lobby"),
    path("group/", views.GroupListCreateAPIView.as_view()),
]
