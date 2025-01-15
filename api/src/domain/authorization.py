class AuthorizationService:
    def __init__(self, user_repository, permission_repository):
        self._user_repository = user_repository
        self._permission_repository = permission_repository

    def has_permission(self, user_id, permission_code):
        """
        Проверяет, есть ли у пользователя указанное право.
        """
        user = self._user_repository.get_user_by_id(user_id)
        if not user:
            return False

        # Проверяем, есть ли у пользователя право с указанным кодом
        return user.permissions.filter(code=permission_code).exists()

    def can_create_meet(self, user_id):
        """
        Проверяет, может ли пользователь создавать миты.
        """
        return self.has_permission(user_id, 3)  # EDIT = 3

    def can_view_meet(self, user_id):
        """
        Проверяет, может ли пользователь просматривать миты.
        """
        return self.has_permission(user_id, 1)  # READ = 1

    def can_edit_feature(self, user_id, project_id):
        """
        Проверяет, может ли пользователь редактировать фичи в проекте.
        """
        # Здесь можно добавить дополнительную логику для проверки доступа к проекту
        return self.has_permission(user_id, 3)  # EDIT = 3
