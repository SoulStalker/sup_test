from django.urls import path

from src.apps.projects.views import (
    ProjectsView,
    CreateProjectView,
    EditProjectView,
    DeleteProjectView,
    SearchProjectView,
    FeaturesView,
)

app_name = "apps.projects"

urlpatterns = [
    path("", ProjectsView.as_view(), name="projects"),
    path("create/", CreateProjectView.as_view(), name="create_project"),
    path("edit/<int:project_id>/", EditProjectView.as_view(), name="edit_project"),
    path("delete/<int:project_id>/", DeleteProjectView.as_view(), name="delete_project"),
    path("search/", SearchProjectView.as_view(), name="search_project"),
    path("Features/", FeaturesView.as_view(), name="Features"),
]
