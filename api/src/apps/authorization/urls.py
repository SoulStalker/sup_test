from django.urls import path
from src.apps.authorization.views import UserAuthorization, UserLogout

app_name = "apps.authorization"

urlpatterns = [
    path("", UserAuthorization.as_view(), name="authorization"),
    path("logout/", UserLogout.as_view(), name="logout"),
]
