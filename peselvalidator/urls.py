from django.urls import path
from peselvalidator import views

app_name = "peselvalidator"


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]