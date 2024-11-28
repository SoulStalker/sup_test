from django.urls import path
from src.apps.users.views import (
    PermissionCreateView,
    PermissionListView,
    PermissionUpdateView,
    RoleCreateView,
    RoleEditView,
    RoleListView,
    UserCreateView,
    UserListView,
    UserPasswordChangeView,
    UserUpdateView,
    UserRegistration,
)

app_name = "apps.users"

urlpatterns = [
    path("registration/", UserRegistration.as_view(), name="registration"),
    path("users/create/", UserCreateView.as_view(), name="create_user"),
    path("", UserListView.as_view(), name="users"),
    path("create/", UserCreateView.as_view(), name="create_user"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update_user"),
    path(
        "password/<int:pk>/",
        UserPasswordChangeView.as_view(),
        name="update_password",
    ),
    # roles
    path("roles/", RoleListView.as_view(), name="roles"),
    path("roles/create/", RoleCreateView.as_view(), name="create_role"),
    path("roles/edit/<int:pk>/", RoleEditView.as_view(), name="update_role"),
    path("roles/delete/<int:pk>/", RoleEditView.as_view(), name="delete_role"),
    # permissions
    path("permissions/", PermissionListView.as_view(), name="permissions"),
    path(
        "permissions/create/",
        PermissionCreateView.as_view(),
        name="create_permission",
    ),
    path(
        "permissions/update/<int:pk>/",
        PermissionUpdateView.as_view(),
        name="update_permission",
    ),
    path(
        "permissions/delete/<int:pk>/",
        PermissionUpdateView.as_view(),
        name="delete_permission",
    ),
]
