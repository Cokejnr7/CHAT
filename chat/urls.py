from django.urls import path

from . import views

urlpatterns = [
    path("", views.lobby),
    path("group/", views.GroupListCreateAPIView.as_view()),
]
