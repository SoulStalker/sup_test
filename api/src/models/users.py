from apps.users.managers import CustomUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from validators.validators import (
    ColorValidator,
    CustomValidator,
    LettersAndSymbolsValidator,
    LettersOnlyValidator,
)


class Role(models.Model):
    """Модель роли пользователя."""

    name = models.CharField(
        max_length=20,
        validators=[LettersOnlyValidator.get_regex_validator()],
        verbose_name="Название",
        help_text="Введите название роли до 20 символов(допускаются только буквы кириллицы и латиницы.)",
    )
    color = models.CharField(
        max_length=6,
        validators=[ColorValidator.get_regex_validator()],
        verbose_name="Цвет",
        help_text="Введите цвет в формате 6 цифр.",
    )

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Permission(models.Model):
    """Модель прав пользователя."""

    name = models.CharField(
        max_length=20,
        validators=[LettersOnlyValidator.get_regex_validator()],
        verbose_name="Название",
    )
    code = models.IntegerField(verbose_name="Код")
    description = models.TextField(
        max_length=500, null=True, blank=True, verbose_name="Описание"
    )

    class Meta:
        verbose_name = "право"
        verbose_name_plural = "права"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""

    name = models.CharField(
        max_length=20,
        validators=[LettersOnlyValidator.get_regex_validator()],
        verbose_name="Имя",
    )
    surname = models.CharField(
        max_length=20,
        validators=[LettersOnlyValidator.get_regex_validator()],
        verbose_name="Фамилия",
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        validators=[CustomValidator.get_regex_validator()],
        verbose_name="Email",
    )
    tg_name = models.CharField(
        max_length=50,
        unique=True,
        validators=[LettersAndSymbolsValidator.get_regex_validator()],
        verbose_name="TG Имя",
    )
    tg_nickname = models.CharField(
        max_length=50,
        unique=True,
        validators=[CustomValidator.get_regex_validator()],
        verbose_name="TG Ник",
    )
    google_meet_nickname = models.CharField(
        max_length=50,
        unique=True,
        validators=[CustomValidator.get_regex_validator()],
        verbose_name="GoogleMeet Ник",
    )
    gitlab_nickname = models.CharField(
        max_length=50,
        unique=True,
        validators=[CustomValidator.get_regex_validator()],
        verbose_name="GitLab Ник",
    )
    github_nickname = models.CharField(
        max_length=50,
        unique=True,
        validators=[CustomValidator.get_regex_validator()],
        verbose_name="GitHub Ник",
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, null=True, verbose_name="Роль"
    )
    permissions = models.ForeignKey(
        Permission, on_delete=models.PROTECT, null=True, verbose_name="Права"
    )
    is_active = models.BooleanField(
        default=False, blank=True, null=True, verbose_name="Активный статус"
    )
    is_admin = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Статус администратора",
    )
    is_superuser = models.BooleanField(
        default=False, verbose_name="Суперпользователь"
    )
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.surname} {self.email}"


class CustomUserList(models.Model):
    """Модель списка пользователей."""

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    registration_date = models.DateField(
        auto_now_add=True, verbose_name="дата создания", null=True, blank=True
    )

    class Meta:
        verbose_name = "пользовательский список"
        verbose_name_plural = "пользовательские списки"
