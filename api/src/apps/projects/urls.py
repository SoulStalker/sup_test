from django.urls import path
from src.apps.projects.views import (
    CreateProjectView,
    EditProjectView,
    ProjectsView,
)

app_name = "apps.projects"

urlpatterns = [
    path("", ProjectsView.as_view(), name="projects"),
    path("create/", CreateProjectView.as_view(), name="create_project"),
    path(
        "edit/<int:project_id>/",
        EditProjectView.as_view(),
        name="edit_project",
    ),
]
