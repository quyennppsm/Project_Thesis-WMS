from django.urls import path

from controller import views

urlpatterns = [
    path("", views.index, name="index"),
]