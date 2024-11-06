from django.http import JsonResponse
from src.apps.custom_view import BaseView
from src.apps.users.forms import (
    CustomUserForm,
    PasswordChangeForm,
    PermissionsForm,
    RoleForm,
)
from src.domain.user.dtos import PermissionDTO, RoleDTO, UserDTO


class RoleListView(BaseView):
    """Список ролей."""

    def get(self, *args, **kwargs):
        roles = self.role_service.get_role_list()

        return JsonResponse({"roles": [vars(role) for role in roles]})


class RoleDetailView(BaseView):
    """Просмотр роли."""

    def get(self, *args, **kwargs):
        role_id = kwargs.get("role_id")
        role = self.role_service.get_role(role_id)

        return JsonResponse(role)


class RoleCreateView(BaseView):
    """Создание роли."""

    def post(self, request):
        form = RoleForm(request.POST)
        if form.is_valid():
            self.role_service.create(
                RoleDTO(
                    name=form.cleaned_data["name"],
                    color=form.cleaned_data["color"],
                )
            )
            return JsonResponse({"status": "success"}, status=201)
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class RoleUpdateView(BaseView):
    """Редактирование роли."""

    def post(self, request, *args, **kwargs):
        role_id = kwargs.get("role_id")
        form = RoleForm(request.POST)

        if form.is_valid():
            self.role_service.update(
                role_id=role_id,
                dto=RoleDTO(
                    name=form.cleaned_data["name"],
                    color=form.cleaned_data["color"],
                ),
            )

            return JsonResponse(
                {"status": "success", "message": "Role updated"}, status=200
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class RoleDeleteView(BaseView):
    """Удаление роли."""

    def delete(self, *args, **kwargs):
        role_id = kwargs.get("role_id")
        try:
            self.role_service.delete(role_id)
            return JsonResponse(
                {"status": "success", "message": "Role deleted"}, status=200
            )
        except Exception as err:
            return JsonResponse(
                {"status": "error", "message": str(err)}, status=404
            )


class PermissionListView(BaseView):
    """Список разрешений."""

    def get(self, *args, **kwargs):
        permissions = self.permission_service.get_permission_list()

        return JsonResponse(
            {"permissions": [vars(permission) for permission in permissions]}
        )


class PermissionDetailView(BaseView):
    """Просмотр разрешения."""

    def get(self, *args, **kwargs):
        permission_id = kwargs.get("permission_id")
        permission = self.permission_service.get_permission(permission_id)

        return JsonResponse(permission)


class PermissionCreateView(BaseView):
    """Создание разрешения."""

    def post(self, request):
        form = PermissionsForm(request.post)
        if form.is_valid():
            self.permission_service.create(
                PermissionDTO(
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["description"],
                    code=form.cleaned_data["code"],
                )
            )

            return JsonResponse({"status": "success"}, status=201)
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class PermissionUpdateView(BaseView):
    """Редактирование разрешения."""

    def post(self, request, *args, **kwargs):
        permission_id = kwargs.get("permission_id")
        form = PermissionsForm(request.POST)

        if form.is_valid():
            self.permission_service.update(
                permission_id=permission_id,
                dto=PermissionDTO(
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["description"],
                    code=form.cleaned_data["code"],
                ),
            )
            return JsonResponse({"status": "success"}, status=200)
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class PermissionDeleteView(BaseView):
    """Удаление разрешения."""

    def delete(self, *args, **kwargs):
        permission_id = kwargs.get("permission_id")
        try:
            self.permission_service.delete(permission_id)
            return JsonResponse(
                {"status": "success", "message": "permission deleted"},
                status=200,
            )
        except Exception as err:
            return JsonResponse(
                {"status": "error", "message": str(err)}, status=404
            )


class UserListView(BaseView):
    """Список пользователей."""

    def get(self, *args, **kwargs):
        users = self.user_service.get_user_list()

        return JsonResponse({"users": [vars(user) for user in users]})


class UserDetailView(BaseView):
    """Просмотр пользователя."""

    def get(self, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = self.user_service.get_user(user_id)

        return JsonResponse(user)


class UserCreateView(BaseView):
    """Создание пользователя."""

    def post(self, request, *args, **kwargs):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user_dto = UserDTO(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                email=form.cleaned_data["email"],
                role_id=form.cleaned_data["role"].id,
                permission_id=form.cleaned_data["permission"].id,
                is_active=form.cleaned_data["is_active"],
                is_staff=form.cleaned_data["is_staff"],
                is_superuser=form.cleaned_data["is_superuser"],
                is_admin=form.cleaned_data["is_admin"],
                name=form.cleaned_data["name"],
                surname=form.cleaned_data["surname"],
                tg_name=form.cleaned_data["tg_name"],
                tg_nickname=form.cleaned_data["tg_nickname"],
                google_meet_nickname=form.cleaned_data["google_meet_nickname"],
                gitlab_nickname=form.cleaned_data["gitlab_nickname"],
                github_nickname=form.cleaned_data["github_nickname"],
                avatar=form.cleaned_data["avatar"],
            )
            generated_password = (
                self.user_service.create_user_with_generated_password(user_dto)
            )
            return JsonResponse(
                {
                    "status": "success",
                    "generated_password": generated_password,
                },
                status=201,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class UserUpdateView(BaseView):
    """Редактирование пользователя."""

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        try:
            form = CustomUserForm(request.POST)
            if form.is_valid():
                self.user_service.update(
                    user_id=user_id,
                    dto=UserDTO(
                        username=form.cleaned_data["username"],
                        password=form.cleaned_data["password"],
                        email=form.cleaned_data["email"],
                        role_id=form.cleaned_data["role"].id,
                        permission_id=form.cleaned_data["permission"].id,
                        is_active=form.cleaned_data["is_active"],
                        is_staff=form.cleaned_data["is_staff"],
                        is_superuser=form.cleaned_data["is_superuser"],
                        is_admin=form.cleaned_data["is_admin"],
                        name=form.cleaned_data["name"],
                        surname=form.cleaned_data["surname"],
                        tg_name=form.cleaned_data["tg_name"],
                        tg_nickname=form.cleaned_data["tg_nickname"],
                        google_meet_nickname=form.cleaned_data[
                            "google_meet_nickname"
                        ],
                        gitlab_nickname=form.cleaned_data["gitlab_nickname"],
                        github_nickname=form.cleaned_data["github_nickname"],
                        avatar=form.cleaned_data["avatar"],
                    ),
                )
                return JsonResponse({"status": "success"}, status=200)
        except Exception as err:
            return JsonResponse(
                {"status": "error", "message": str(err)}, status=404
            )


class UserDeleteView(BaseView):
    """Удаление пользователя."""

    def delete(self, *args, **kwargs):
        user_id = kwargs.get("user_id")
        try:
            self.user_service.delete(user_id)
            return JsonResponse(
                {"status": "success", "message": "User delete"}, status=200
            )
        except Exception as err:
            return JsonResponse(
                {"status": "error", "message": str(err)}, status=404
            )


class UserPasswordChangeView(BaseView):
    """Смена пароля пользователя."""

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        try:
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                self.user_service.change_password(
                    user_id=user_id,
                    dto=UserDTO(
                        password=form.cleaned_data["password"],
                    ),
                )
                return JsonResponse({"status": "success"}, status=200)
        except Exception as err:
            return JsonResponse(
                {"status": "error", "message": str(err)}, status=404
            )
