from django.urls import path
from src.apps.teams.views import TeamCreateView, TeamListView, TeamUpdateView

app_name = "apps.teams"

urlpatterns = [
    path("", TeamListView.as_view(), name="teams"),
    path("create/", TeamCreateView.as_view(), name="create_team"),
    path("edit/<int:team_id>/", TeamUpdateView.as_view(), name="update_team"),
]
