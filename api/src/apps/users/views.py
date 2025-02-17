from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from src.apps.custom_view import BaseView
from src.apps.users.forms import (
    CreateUserForm,
    PasswordChangeForm,
    PermissionsForm,
    RoleForm,
)
from src.domain.user import CreatePermissionDTO, CreateUserEntity
from src.domain.user.entity import (
    CreateRoleEntity,
    PermissionEntity,
    RoleEntity,
    UserEntity,
)
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
            role = CreateRoleEntity(
                name=form.cleaned_data["name"],
                color=form.cleaned_data["color"],
            )
            return self.handle_form(
                form,
                self.role_service.create,
                role,
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class RoleEditView(BaseView):
    """Редактирование роли."""

    def get(self, request, *args, **kwargs):
        role_id = kwargs.get("pk")
        role, error = self.role_service.get_by_id(role_id, self.user_id)
        if error:
            return JsonResponse(
                {"status": "error", "message": str(error)}, status=403
            )
        data = {
            "name": role.name,
            "color": role.color,
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        role_id = kwargs.get("pk")
        form = RoleForm(request.POST)
        if form.is_valid():
            role_dto = RoleEntity(
                id=role_id,
                name=form.cleaned_data["name"],
                color=form.cleaned_data["color"],
            )
            return self.handle_form(
                form,
                self.role_service.update,
                role_id,
                role_dto,
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )

    def delete(self, *args, **kwargs):
        role_id = kwargs.get("pk")
        try:
            self.role_service.delete(role_id, self.user_id)
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
        # получение данных по типам объектов и объектам прав
        # срабатывает только при выборке типа объекта
        # поэтому сверху чтобы не отрабатывать весь код
        content_type_id = self.request.GET.get("content_type_id")
        if content_type_id:
            objects_data = self.permission_service.get_objects_data(
                content_type_id
            )
            return JsonResponse(objects_data, safe=False)

        # получение списка разрешений
        permissions = self.permission_service.get_list()
        permissions = self.paginate_queryset(permissions)
        content_types = self.permission_service.get_content_types()
        objects = self.permission_service.get_content_objects()
        codes = set(self.permission_service.get_codes())

        return render(
            self.request,
            "permissions/permission_list.html",
            {
                "permissions": permissions,
                "content_types": content_types,
                "objects": objects,
                "codes": codes,
            },
        )


class PermissionCreateView(BaseView):
    """Создание разрешения."""

    def post(self, request, *args, **kwargs):
        form = PermissionsForm(request.POST)

        if form.is_valid():
            permission_dto = CreatePermissionDTO(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                code=form.cleaned_data["code"],
                content_type=form.cleaned_data["content_type"],
                object_id=form.cleaned_data["object_id"],
            )
            return self.handle_form(
                form,
                self.permission_service.create,
                permission_dto,
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class PermissionUpdateView(BaseView):
    """Редактирование разрешения."""

    def get(self, request, *args, **kwargs):
        permission_id = kwargs.get("pk")
        permission, error = self.permission_service.get_by_id(
            permission_id, self.user_id
        )
        if error:
            return JsonResponse(
                {"status": "error", "message": str(error)}, status=403
            )

        data = {
            "id": permission.id,
            "name": permission.name,
            "code": permission.code,
            "description": permission.description,
            "content_type": permission.content_type.id,
            "object": (
                self.permission_service.get_content_object(permission.id)
                if permission.object_id
                else None
            ),
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        permission_id = kwargs.get("pk")
        form = PermissionsForm(request.POST)
        if form.is_valid():
            permission_dto = PermissionEntity(
                id=permission_id,
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                code=form.cleaned_data["code"],
                content_type=form.cleaned_data["content_type"],
                object_id=(
                    form.cleaned_data["object_id"]
                    if form.cleaned_data["object_id"]
                    else None
                ),
            )
            return self.handle_form(
                form,
                self.permission_service.update,
                permission_id,
                permission_dto,
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )

    def delete(self, *args, **kwargs):
        permission_id = kwargs.get("pk")
        try:
            self.permission_service.delete(permission_id, self.user_id)
            return JsonResponse(
                {"status": "success", "message": "Permission deleted"},
                status=200,
            )
        except Exception as err:
            return JsonResponse(
                {"status": "error", "message": str(err)}, status=403
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
        send_email = request.POST.get("send_email", "")
        print(request.POST)

        form = CreateUserForm(request.POST)
        if form.is_valid():
            user_dto = CreateUserEntity(
                name=form.cleaned_data["name"],
                surname=form.cleaned_data["surname"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                tg_name=form.cleaned_data["tg_name"],
                tg_nickname=form.cleaned_data["tg_nickname"],
                google_meet_nickname=form.cleaned_data["google_meet_nickname"],
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
            print(send_email)
            if send_email == "true":
                try:
                    send_email_to_user.delay(
                        name=user_dto.name, email=user_dto.email
                    )
                except Exception as e:
                    return JsonResponse(
                        {
                            "status": "error",
                            "errors": f"Email не отправлен: {str(e)}",
                        },
                        status=400,
                    )
            return self.handle_form(
                form,
                self.user_service.create,
                user_dto,
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class UserUpdateView(BaseView):
    """Редактирование пользователя."""

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user, error = self.user_service.get_by_id(user_id, self.user_id)
        if error:
            return JsonResponse(
                {"status": "error", "message": str(error)}, status=403
            )
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
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user_dto = UserEntity(
                    id=user_id,
                    name=form.cleaned_data["name"],
                    surname=form.cleaned_data["surname"],
                    email=form.cleaned_data["email"],
                    password=(
                        form.cleaned_data["password"]
                        if "password" in form
                        else None
                    ),
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
                    is_superuser=form.cleaned_data.get("is_superuser", False),
                    date_joined=form.cleaned_data.get("date_joined", None),
                    meet_statuses=None,
                )
                return self.handle_form(
                    form,
                    self.user_service.update,
                    user_id,
                    user_dto,
                    self.user_id,
                )
            return JsonResponse(
                {"status": "error", "errors": form.errors}, status=400
            )


class UserPasswordChangeView(BaseView):
    """Смена пароля пользователя."""

    def get(self, request, *args, **kwargs):
        return render(request, "password_change.html")

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            form = PasswordChangeForm(request.POST, user=user)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("users:personal_account"))
            error_message = [
                error
                for field, errors in form.errors.items()
                for error in errors
            ]
            return render(
                request,
                "password_change.html",
                {"form": form, "error_message": error_message},
            )
        except Exception as err:
            return JsonResponse(
                {"status": "error", "message": str(err)}, status=400
            )


class ProfileView(BaseView):
    def get(self, request, *args, **kwargs):
        roles = self.role_service.get_list()
        permissions = self.permission_service.get_list()
        teams = self.team_service.get_list()
        user, error = self.user_service.get_by_id(self.user_id, self.user_id)
        if error:
            return JsonResponse(
                {"status": "error", "message": str(error)}, status=403
            )
        return render(
            self.request,
            "users/profile.html",
            {
                "user": user,
                "roles": roles,
                "permissions": permissions,
                "teams": teams,
            },
        )
