from django.urls import path
from src.apps.auth_app.views import login_view, logout_view

app_name = "apps.auth_app"

urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
