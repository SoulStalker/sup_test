from django.http import JsonResponse
from src.apps.custom_view import BaseView
from src.apps.users.forms import PermissionsForm, RoleForm
from src.domain.user.dtos import PermissionDTO, RoleDTO


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
        form = RoleForm(request.post)
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
