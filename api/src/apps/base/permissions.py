from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

user = get_user_model()


class PermissionMixin:
    """
    Миксин для проверки прав доступа пользователя.
    """

    def has_permission(self, user_id: int, action, obj=None) -> bool:
        """
        Проверка наличия прав у пользователя на выполнение действия.
        :param user_id: ID пользователя
        :param action: код действия (например, 1, 2, 3)
        :param obj: объект, для которого проверяются права (например, Meet)
        :return: bool
        """
        current_user = get_object_or_404(user, pk=user_id)
        # Если пользователь является суперпользователем, возвращаем True
        if current_user.is_superuser:
            return True

        content_type = ContentType.objects.get_for_model(self.model)
        object_id = obj.id if obj else None

        # Проверяем права на конкретный объект (если object_id указан)
        if object_id is not None:
            permissions = current_user.permissions.filter(
                content_type=content_type,
                object_id=object_id,
            ).values_list(
                "code", flat=True
            )  # Достаём числовые коды

            if permissions and max(permissions) >= action:
                return True

        # Если права на конкретный объект не найдены, проверяем глобальные права
        global_permissions = current_user.permissions.filter(
            content_type=content_type,
            object_id=None,
        ).values_list(
            "code", flat=True
        )  # Достаём числовые коды

        if global_permissions and max(global_permissions) >= action:
            return True

        return False
