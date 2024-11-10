from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from src.models.managers import CustomUserManager
from ..domain.validators.validators import ModelValidator


class Role(models.Model):
    """Модель роли пользователя."""

    name = models.CharField(
        max_length=20,
        validators=[ModelValidator.validate_letters_only],
        verbose_name="название",
        help_text="Введите название роли до 20 символов(допускаются только буквы кириллицы и латиницы.",
    )
    color = models.CharField(
        max_length=6,
        validators=[ModelValidator.validate_color],
        verbose_name="цвет",
        help_text="Введите цвет в формате 6 цифр.",
    )

    class Meta:
        verbose_name = "роль"
        verbose_name_plural = "роли"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Permission(models.Model):
    """Модель прав пользователя."""

    name = models.CharField(
        max_length=20,
        validators=[ModelValidator.validate_letters_only],
        verbose_name="название",
    )
    code = models.IntegerField(verbose_name="код")
    description = models.TextField(
        max_length=500, null=True, blank=True, verbose_name="описание"
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
        validators=[ModelValidator.validate_letters_only()],
        verbose_name="имя",
    )
    surname = models.CharField(
        max_length=20,
        validators=[ModelValidator.validate_letters_only()],
        verbose_name="фамилия",
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        validators=[ModelValidator.validate_email()],
        verbose_name="email",
    )
    tg_name = models.CharField(
        max_length=50,
        unique=True,
        validators=[ModelValidator.validate_letter_digits_symbols()],
        verbose_name="tg имя",
    )
    tg_nickname = models.CharField(
        max_length=50,
        unique=True,
        validators=[ModelValidator.validate_letter_digits_symbols()],
        verbose_name="tg ник",
    )
    google_meet_nickname = models.CharField(
        max_length=50,
        unique=True,
        validators=[ModelValidator.validate_letter_digits_symbols()],
        verbose_name="googlemeet ник",
    )
    gitlab_nickname = models.CharField(
        max_length=50,
        unique=True,
        validators=[ModelValidator.validate_letter_digits_symbols()],
        verbose_name="gitlab ник",
    )
    github_nickname = models.CharField(
        max_length=50,
        unique=True,
        validators=[ModelValidator.validate_letter_digits_symbols()],
        verbose_name="github ник",
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="аватар"
    )
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, null=True, verbose_name="роль"
    )
    permissions = models.ForeignKey(
        Permission, on_delete=models.PROTECT, null=True, verbose_name="права"
    )
    is_active = models.BooleanField(
        default=False, blank=True, null=True, verbose_name="активный статус"
    )
    is_admin = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="статус администратора",
    )
    is_superuser = models.BooleanField(
        default=False, verbose_name="суперпользователь"
    )
    is_staff = models.BooleanField(default=False, verbose_name="персонал")

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
        auto_now_add=True, verbose_name="дата создания"
    )

    class Meta:
        verbose_name = "пользовательский список"
        verbose_name_plural = "пользовательские списки"
