from django.urls import path

from textshuffle import views

app_name = "textshuffle"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]