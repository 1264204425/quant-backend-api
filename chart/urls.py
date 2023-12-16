from django import views
from django.urls import path
from . import views

urlpatterns = [
    path("ahr999/", views.ahr999_view),
]