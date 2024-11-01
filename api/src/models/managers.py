from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Менеджер для создания и управления пользователями."""

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Введите email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError(
                "Суперпользователь должен иметь флаг is_admin=True"
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Суперпользователь должен иметь флаг is_superuser=True"
            )
        return self.create_user(email, password, **extra_fields)
