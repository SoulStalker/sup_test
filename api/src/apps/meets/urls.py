from django.urls import path

from src.apps.meets.views import CreateMeetView, MeetsView, EditMeetView, CategoryView

app_name = "apps.meets"

urlpatterns = [
    path("", MeetsView.as_view(), name="meets"),
    path("delete/<int:meet_id>/", MeetsView.as_view(), name="delete_meet"),
    path("create/", CreateMeetView.as_view(), name="create_meet"),
    path("edit/<int:meet_id>/", EditMeetView.as_view(), name="edit_meet"),
    path('add-category/', CategoryView.as_view(), name='add_category'),
]
