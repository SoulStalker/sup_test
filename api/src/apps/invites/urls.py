from django.urls import path
from src.apps.invites.views import InvitesView

app_name = "apps.invites"

urlpatterns = [
    path("", InvitesView.as_view(), name="invite"),
    path("create_invite/", InvitesView.as_view(), name="create_invite"),
    path("delete/<int:meet_id>/", InvitesView.as_view(), name="delete_invite"),
]
