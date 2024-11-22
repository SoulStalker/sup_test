from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.users.forms import (
    CustomUserForm,
    PasswordChangeForm,
    PermissionsForm,
    RoleForm,
)
from src.domain.user.dtos import (
    CreatePermissionDTO,
    CreateRoleDTO,
    PermissionDTO,
    RoleDTO,
    UserDTO,
)


class RoleListView(BaseView):
    """Список ролей."""

    def get(self, *args, **kwargs):
        roles = self.role_service.get_role_list()
        for role in roles:
            role.participants = self.role_service.get_roles_participants_count(
                role.id
            )
        # return JsonResponse({"roles": [vars(role) for role in roles]})
        return render(self.request, "roles/roles_list.html", {"roles": roles})


class RoleCreateView(BaseView):
    """Создание роли."""

    def post(self, request):
        form = RoleForm(request.POST)
        if form.is_valid():
            try:
                self.role_service.create(
                    CreateRoleDTO(
                        name=form.cleaned_data["name"],
                        color=form.cleaned_data["color"],
                    )
                )
                return JsonResponse({"status": "success"}, status=201)
            except IntegrityError:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Такая роль уже существует",
                    },
                    status=400,
                )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class RoleEditView(BaseView):
    """Редактирование роли."""

    def get(self, request, *args, **kwargs):
        role_id = kwargs.get("pk")
        role = self.role_service.get_role(role_id)

        data = {
            "name": role.name,
            "color": role.color,
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        try:
            role_id = kwargs.get("pk")
            form = RoleForm(request.POST)

            if form.is_valid():
                self.role_service.update(
                    role_id=role_id,
                    dto=RoleDTO(
                        id=role_id,
                        name=form.cleaned_data["name"],
                        color=form.cleaned_data["color"],
                    ),
                )

                return JsonResponse(
                    {"status": "success", "message": "Role updated"},
                    status=201,
                )
        except IntegrityError:
            return JsonResponse(
                {"status": "error", "message": "Такая роль уже существует"},
                status=400,
            )

    def delete(self, *args, **kwargs):
        role_id = kwargs.get("pk")
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
        # return JsonResponse({"roles": [vars(role) for role in roles]})
        return render(
            self.request,
            "permissions/permission_list.html",
            {"permissions": permissions},
        )


class PermissionCreateView(BaseView):
    """Создание разрешения."""

    def post(self, request, *args, **kwargs):

        print(request.POST)

        form = PermissionsForm(request.POST)

        if form.is_valid():
            try:
                self.permission_service.create(
                    CreatePermissionDTO(
                        name=form.cleaned_data["name"],
                        description=form.cleaned_data["description"],
                        code=form.cleaned_data["code"],
                    )
                )
            except Exception as err:
                print(err)
            return JsonResponse({"status": "success"}, status=201)
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class PermissionUpdateView(BaseView):
    """Редактирование разрешения."""

    def get(self, request, *args, **kwargs):
        permission_id = kwargs.get("pk")
        permission = self.permission_service.get_permission(permission_id)

        data = {
            "id": permission.id,
            "name": permission.name,
            "code": permission.code,
            "description": permission.description,
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        permission_id = kwargs.get("pk")
        form = PermissionsForm(request.POST)
        if form.is_valid():
            try:
                self.permission_service.update(
                    permission_id=permission_id,
                    dto=PermissionDTO(
                        id=permission_id,
                        name=form.cleaned_data["name"],
                        description=form.cleaned_data["description"],
                        code=form.cleaned_data["code"],
                    ),
                )
            except Exception as err:
                print(err)
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

        # return JsonResponse({"users": [user.name for user in users]})
        return render(self.request, "users_list.html", {"users": users})


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
                username=form.cleaned_data["name"],
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
                        username=form.cleaned_data["name"],
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
