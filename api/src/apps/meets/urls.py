from django.urls import path

from src.apps.meets.views import CreateMeetView, MeetsView

app_name = "apps.meets"

urlpatterns = [
    path("", MeetsView.as_view(), name="meets"),
    path("delete/<int:meet_id>/", MeetsView.as_view(), name="delete_meet"),
    path("create/", CreateMeetView.as_view(), name="create_meet"),
]
