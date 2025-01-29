from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from src.models.managers import CustomUserManager

from .validators import ModelValidator


class Role(models.Model):
    """Модель роли пользователя."""

    name = models.CharField(
        max_length=20,
        validators=[ModelValidator.validate_letters_only()],
        verbose_name="название",
        help_text="Введите название роли до 20 символов(допускаются только буквы кириллицы и латиницы.",
    )
    color = models.CharField(
        max_length=6,
        validators=[ModelValidator.validate_color()],
        verbose_name="цвет",
        help_text="Введите цвет в формате 6 цифр.",
    )

    class Meta:
        verbose_name = "роль"
        verbose_name_plural = "роли"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name="Команда",
        validators=[ModelValidator.validate_letters_space_only()],
        unique=True,
    )
    participants = models.ManyToManyField(
        to="CustomUser",
        related_name="team_participants",
        verbose_name="Участники",
    )

    class Meta:
        verbose_name = "команда"
        verbose_name_plural = "команды"
        ordering = ["name"]

    def __str__(self):
        return self.name


class PermissionCodes(models.IntegerChoices):
    """Класс для определения кодов прав."""

    READ = 1, "Чтение"
    COMMENT = 2, "Комментирование"
    EDIT = 3, "Редактирование"


class Permission(models.Model):
    """Модель прав пользователя."""

    name = models.CharField(
        max_length=50, unique=True, verbose_name="Название"
    )
    code = models.IntegerField(
        choices=PermissionCodes.choices, verbose_name="Код доступа"
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание"
    )

    # Связь с объектами
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Тип объекта",
        related_name="permissions",
    )
    object_id = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="ID объекта"
    )
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "право"
        verbose_name_plural = "права"
        ordering = ["-id"]
        unique_together = ("code", "content_type", "object_id")

    def __str__(self):
        obj_info = f" | {self.content_object}" if self.content_object else ""
        return f"{self.name} ({self.code}){obj_info}"


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
    password = models.CharField(
        max_length=150,
        validators=[ModelValidator.validate_password()],
        verbose_name="пароль",
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
        upload_to="images/avatars/",
        blank=True,
        null=True,
        verbose_name="аватар",
    )
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, verbose_name="роль"
    )
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, verbose_name="команда"
    )
    permissions = models.ManyToManyField(
        to=Permission,
        related_name="customuser_permissions",
        verbose_name="права",
        blank=True,
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
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="дата регистрации"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
        "surname",
        "tg_name",
        "tg_nickname",
        "google_meet_nickname",
        "gitlab_nickname",
        "github_nickname",
    ]
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} {self.surname} {self.email}"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()


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
