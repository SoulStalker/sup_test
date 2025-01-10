from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.users.forms import (
    CreateUserForm,
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
from src.domain.user.entity import CreateUserEntity
from src.services.tasks import send_email_to_user


class RoleListView(BaseView):
    """Список ролей."""

    def get(self, *args, **kwargs):
        roles = self.role_service.get_list()
        roles = self.paginate_queryset(roles)
        for role in roles:
            role.participants = self.role_service.get_roles_participants_count(
                role.id
            )
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
        role = self.role_service.get_by_id(role_id)

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
        permissions = self.permission_service.get_list()
        permissions = self.paginate_queryset(permissions)
        return render(
            self.request,
            "permissions/permission_list.html",
            {"permissions": permissions},
        )


class PermissionCreateView(BaseView):
    """Создание разрешения."""

    def post(self, request, *args, **kwargs):
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
        permission = self.permission_service.get_by_id(permission_id)

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

    def delete(self, *args, **kwargs):
        permission_id = kwargs.get("pk")
        try:
            self.permission_service.delete(permission_id)
            return JsonResponse(
                {"status": "success", "message": "Permission deleted"},
                status=200,
            )
        except Exception as err:
            return JsonResponse(
                {"status": "error", "message": str(err)}, status=404
            )


class UserListView(BaseView):
    """Список пользователей."""

    def get(self, *args, **kwargs):
        roles = self.role_service.get_list()
        permissions = self.permission_service.get_list()
        teams = self.team_service.get_list()

        users = self.user_service.get_list()
        users = self.paginate_queryset(users)

        return render(
            self.request,
            "users/users_list.html",
            {
                "users": users,
                "roles": roles,
                "permissions": permissions,
                "teams": teams,
            },
        )


class UserCreateView(BaseView):
    """Создание пользователя."""

    def post(self, request, *args, **kwargs):
        send_email = request.POST.get("send_email", False)

        form = CreateUserForm(request.POST)
        if form.is_valid():
            user_dto = self.user_service.create(
                CreateUserEntity(
                    name=form.cleaned_data["name"],
                    surname=form.cleaned_data["surname"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                    tg_name=form.cleaned_data["tg_name"],
                    tg_nickname=form.cleaned_data["tg_nickname"],
                    google_meet_nickname=form.cleaned_data[
                        "google_meet_nickname"
                    ],
                    gitlab_nickname=form.cleaned_data["gitlab_nickname"],
                    github_nickname=form.cleaned_data["github_nickname"],
                    avatar=(
                        request.FILES["avatar"]
                        if "avatar" in request.FILES
                        else None
                    ),
                    role_id=form.cleaned_data["role"].id,
                    team_id=(
                        form.cleaned_data["team"].id
                        if form.cleaned_data["team"]
                        else None
                    ),
                    permissions_ids=[
                        int(permission.id)
                        for permission in form.cleaned_data["permissions"]
                    ],
                    is_active=form.cleaned_data.get("is_active", False),
                    is_admin=form.cleaned_data.get("is_admin", False),
                    is_superuser=form.cleaned_data.get("is_superuser", False),
                )
            )

            if send_email:
                try:
                    send_email_to_user.delay(
                        name=user_dto.name, email=user_dto.email
                    )
                except Exception as e:
                    print(f"Email не отправлен: {str(e)}")
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": f"Email не отправлен: {str(e)}",
                        },
                        status=400,
                    )

            return JsonResponse(
                {"status": "success", "message": "email sent"},
                status=201,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class UserUpdateView(BaseView):
    """Редактирование пользователя."""

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = self.user_service.get_by_id(user_id)
        data = {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "tg_name": user.tg_name,
            "tg_nickname": user.tg_nickname,
            "google_meet_nickname": user.google_meet_nickname,
            "gitlab_nickname": user.gitlab_nickname,
            "github_nickname": user.github_nickname,
            "avatar": user.avatar.url if user.avatar else None,
            "role_id": user.role_id.id if user.role_id else None,
            "team_id": user.team_id.id if user.team_id else None,
            "permissions_ids": user.permissions_ids,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        try:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                self.user_service.update(
                    user_id=user_id,
                    dto=UserDTO(
                        id=user_id,
                        name=form.cleaned_data["name"],
                        surname=form.cleaned_data["surname"],
                        email=form.cleaned_data["email"],
                        tg_name=form.cleaned_data["tg_name"],
                        tg_nickname=form.cleaned_data["tg_nickname"],
                        google_meet_nickname=form.cleaned_data[
                            "google_meet_nickname"
                        ],
                        gitlab_nickname=form.cleaned_data["gitlab_nickname"],
                        github_nickname=form.cleaned_data["github_nickname"],
                        avatar=(
                            request.FILES["avatar"]
                            if "avatar" in request.FILES
                            else None
                        ),
                        role_id=form.cleaned_data["role"],
                        team_id=form.cleaned_data.get("team", None),
                        permissions_ids=[
                            int(permission.id)
                            for permission in form.cleaned_data["permissions"]
                        ],
                        is_active=form.cleaned_data.get("is_active", False),
                        is_admin=form.cleaned_data.get("is_admin", False),
                        is_superuser=form.cleaned_data.get(
                            "is_superuser", False
                        ),
                        date_joined=form.cleaned_data.get("date_joined", None),
                        meet_statuses=None,
                    ),
                )

                return JsonResponse({"status": "success"}, status=200)
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
