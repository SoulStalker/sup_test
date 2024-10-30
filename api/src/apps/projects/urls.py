from django.urls import path

from src.apps.projects.views import (
    ProjectsView,
)

app_name = "apps.projects"

urlpatterns = [
    path("", ProjectsView.as_view(), name="projects"),
]
