from django.urls import path
from src.apps.invites.views import InvitesView

app_name = "apps.invites"

urlpatterns = [
    path("", InvitesView.as_view(), name="invite"),
]
