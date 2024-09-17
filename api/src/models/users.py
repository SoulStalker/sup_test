from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from apps.users.managers import CustomUserManager
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
    color = models.IntegerField(
        max_length=6,
        validators=[ColorValidator.get_regex_validator()],
        verbose_name="Цвет",
        help_text="Введите цвет в формате 6 цифр.",
    )

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = -id

    def __str__(self):
        return self.name


class Permissions(models.Model):
    """Модель прав пользователя."""

    name = models.CharField(
        max_length=20,
        validators=[LettersOnlyValidator.get_regex_validator()],
        verbose_name="Название",
    )
    code = models.IntegerField(max_length=6, verbose_name="Код")
    description = models.TextField(
        max_length=500, null=True, blank=True, verbose_name="Описание"
    )

    class Meta:
        verbose_name = "право"
        verbose_name_plural = "права"
        ordering = -id

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser):
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
        Role, on_delete=models.CASCADE, verbose_name="Роль"
    )
    permissions = models.ForeignKey(
        Permissions, on_delete=models.PROTECT, verbose_name="Права"
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

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = -id

    def __str__(self):
        return f"{self.name} {self.surname} {self.email}"
