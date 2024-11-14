from django.urls import path
from src.apps.users.views import (
    RoleCreateView,
    RoleDeleteView,
    RoleDetailView,
    RoleListView,
    RoleUpdateView,
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
    path("role/create/", RoleCreateView.as_view(), name="create_role"),
    path("role/update<int:pk>/", RoleUpdateView.as_view(), name="update_role"),
    path("roles/", RoleListView.as_view(), name="roles"),
    path(
        "role/delete/<int:pk>/", RoleDeleteView.as_view(), name="delete_role"
    ),
    path("role/<int:pk>/", RoleDetailView.as_view(), name="role_detail"),
    path("permissions/", RoleListView.as_view(), name="permissions"),
    path(
        "permissions/<int:pk>/",
        RoleDetailView.as_view(),
        name="permission_detail",
    ),
    path(
        "permissions/create/",
        RoleCreateView.as_view(),
        name="create_permission",
    ),
    path(
        "permissions/update/<int:pk>/",
        RoleUpdateView.as_view(),
        name="update_permission",
    ),
    path(
        "permissions/delete/<int:pk>/",
        RoleDeleteView.as_view(),
        name="delete_permission",
    ),
]
