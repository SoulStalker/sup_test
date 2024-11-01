from django.urls import path
from src.apps.users.views import (
    ChangePasswordView,
    SignUpView,
    UserListView,
    UserLogin,
)

app_name = "apps.users"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UserLogin.as_view(), name="login"),
    path("password/", ChangePasswordView.as_view(), name="change_password"),
    path("users/", UserListView.as_view(), name="users"),
]
