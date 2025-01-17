# class AuthorizationService:
#     def __init__(self, user):
#         self.user = user
#
#     def has_permission(self, action: str, obj=None) -> bool:
#         """
#         Проверка наличия разрешения у пользователя.
#         - action: код действия, например, "EDIT_TASK".
#         - obj: объект, для которого проверяется разрешение. Если None, проверяется глобальное разрешение.
#         """
#         permissions = Permission.objects.filter(user=self.user, code=action)
#
#         if obj:
#             content_type = ContentType.objects.get_for_model(obj)
#             permissions = permissions.filter(
#                 content_type=content_type, object_id=obj.id
#             )
#
#         return permissions.exists()
