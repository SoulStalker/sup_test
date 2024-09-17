from django.urls import path

from apps.projects.views import (
    FeatureCreateView,
    FeatureUpdateView,
    ProjectCreateView,
    ProjectUpdateView,
    TagCreateView,
    TagUpdateView,
    TaskCreateView,
    TaskUpdateView,
)

app_name = "apps.projects"

urlpatterns = [
    # Tag views
    path("create-tag/", TagCreateView.as_view(), name="create_tag"),
    path(
        "update-tag/<slug:slug>/", TagUpdateView.as_view(), name="update_tag"
    ),
    # Feature views
    path(
        "create-feature/", FeatureCreateView.as_view(), name="create_feature"
    ),
    path(
        "update-feature/<slug:slug>/",
        FeatureUpdateView.as_view(),
        name="update_feature",
    ),
    # Project views
    path(
        "create-project/", ProjectCreateView.as_view(), name="create_project"
    ),
    path(
        "update-project/<slug:slug>/",
        ProjectUpdateView.as_view(),
        name="update_project",
    ),
    # Task views
    path("create-task/", TaskCreateView.as_view(), name="create_task"),
    path(
        "update-task/<slug:slug>/",
        TaskUpdateView.as_view(),
        name="update_task",
    ),
]
