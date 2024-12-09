from django.urls import path
from src.apps.projects.task import (
    CreateTaskView,
    DeleteTaskView,
    TasksView,
    UpdateTaskView,
)
from src.apps.projects.views import (
    CreateFeatureView,
    CreateProjectView,
    DeleteFeatureView,
    DeleteProjectView,
    EditFeatureView,
    EditProjectView,
    FeaturesView,
    ProjectsView,
    SearchFeatureView,
    SearchProjectView,
)

app_name = "apps.projects"

urlpatterns = [
    # проекты
    path("", ProjectsView.as_view(), name="projects"),
    path("create/", CreateProjectView.as_view(), name="create_project"),
    path(
        "edit/<int:project_id>/",
        EditProjectView.as_view(),
        name="edit_project",
    ),
    path(
        "delete/<int:project_id>/",
        DeleteProjectView.as_view(),
        name="delete_project",
    ),
    path("search/", SearchProjectView.as_view(), name="search_project"),
    # фичи проекта
    path("features/", FeaturesView.as_view(), name="features"),
    path(
        "features/create/", CreateFeatureView.as_view(), name="create_features"
    ),
    path(
        "features/edit/<int:feature_id>/",
        EditFeatureView.as_view(),
        name="edit_features",
    ),
    path(
        "features/delete/<int:feature_id>/",
        DeleteFeatureView.as_view(),
        name="delete_features",
    ),
    path(
        "features/search/", SearchFeatureView.as_view(), name="search_features"
    ),
    # задачи
    path("features/tasks/", TasksView.as_view(), name="tasks"),
    path(
        "features/tasks/create/", CreateTaskView.as_view(), name="create_task"
    ),
    path(
        "features/tasks/update/<int:task_id>/",
        UpdateTaskView.as_view(),
        name="edit_tasks",
    ),
    path(
        "features/tasks/delete/<int:task_id>/",
        DeleteTaskView.as_view(),
        name="delete_tasks",
    ),
]
