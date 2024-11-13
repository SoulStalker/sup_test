from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .choice_classes import MeetStatusChoice
from .validators import ModelValidator

User = get_user_model()


class Category(models.Model):
    """
    Модель категория митов
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Категория",
        validators=[ModelValidator.validate_letters_only()],
    )

    class Meta:
        db_table = "category"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Meet(models.Model):
    """
    Модель самих митов, связана с категорией
    """

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        verbose_name="Категория",
        null=True,
    )
    title = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Название",
        validators=[ModelValidator.validate_letters_space_only()],
    )
    start_time = models.DateTimeField(
        default=timezone.now, verbose_name="Дата"
    )
    author = models.ForeignKey(
        User,
        related_name="author_meets",
        on_delete=models.CASCADE,
        verbose_name="Автор",
        null=True,
    )
    responsible = models.ForeignKey(
        User,
        related_name="responsible_meets",
        on_delete=models.CASCADE,
        verbose_name="Ответственный",
        default=author,
    )
    participants = models.ManyToManyField(
        User,
        through="MeetParticipant",
        related_name="meets",
        verbose_name="Участники",
    )

    class Meta:
        db_table = "meets"
        verbose_name = "Мит"
        verbose_name_plural = "Миты"
        ordering = ["start_time", "category", "title"]

    def __str__(self):
        return f"{self.title} - {self.start_time}"


class MeetParticipant(models.Model):
    """
    Промежуточная модель, связывающая миты и участников
    """

    meet = models.ForeignKey(
        Meet, on_delete=models.CASCADE, verbose_name="Мит"
    )
    custom_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="custom_meets",
        verbose_name="Участник",
    )
    status = models.CharField(
        max_length=10,
        choices=MeetStatusChoice.choices,
        default=MeetStatusChoice.PRESENT,
        verbose_name="Статус",
    )

    class Meta:
        db_table = "custom_user_meet"
        unique_together = ("meet", "custom_user")
        verbose_name = "Участник мита"
        verbose_name_plural = "Участники мита"

    @property
    def status_color(self):
        return MeetStatusChoice.get_color(self.status)

    def __str__(self):
        return (
            f"{self.custom_user.name} - "
            f"{self.status_color} на {self.meet.title}"
        )
