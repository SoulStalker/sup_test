from django.urls import path
from src.apps.users.views import (
    RoleCreateView,
    RoleEditView,
    RoleListView,
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserPasswordChangeView,
    UserUpdateView,
)

app_name = "apps.users"

urlpatterns = [
    path("", UserListView.as_view(), name="users"),
    path("create/", UserCreateView.as_view(), name="create_user"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update_user"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="delete_user"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path(
        "password/<int:pk>/",
        UserPasswordChangeView.as_view(),
        name="update_password",
    ),
    path("roles/", RoleListView.as_view(), name="roles"),
    path("roles/create/", RoleCreateView.as_view(), name="create_role"),
    path("roles/edit/<int:pk>/", RoleEditView.as_view(), name="update_role"),
    path("roles/delete/<int:pk>/", RoleEditView.as_view(), name="delete_role"),
    path("permissions/", RoleListView.as_view(), name="permissions"),
    path(
        "permissions/create/",
        RoleCreateView.as_view(),
        name="create_permission",
    ),
    path(
        "permissions/update/<int:pk>/",
        RoleEditView.as_view(),
        name="update_permission",
    ),
]
