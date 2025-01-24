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
        :param action: код действия (например, "EDIT", "READ", "COMMENT")
        :param obj: объект, для которого проверяются права (например, Meet)
        :return: bool
        """
        content_type = ContentType.objects.get_for_model(self.model)
        object_id = obj.id if obj else None

        current_user = get_object_or_404(user, pk=user_id)

        # Проверяем права на конкретный объект (если object_id указан)
        if object_id is not None:
            permissions = current_user.permissions.filter(
                content_type=content_type,
                object_id=object_id,
            ).values_list("code", flat=True)
            if permissions:
                return max(permissions) >= action

        # Если права на конкретный объект не найдены, проверяем права на все объекты (object_id = None)
        global_permissions = current_user.permissions.filter(
            content_type=content_type,
            object_id=None,  # Права на все объекты
        ).values_list("code", flat=True)

        # Если есть права на все объекты, возвращаем True, если максимальное право >= action
        if global_permissions:
            return max(global_permissions) >= action

        # Если ни одно из условий не выполнено, возвращаем False
        return False
