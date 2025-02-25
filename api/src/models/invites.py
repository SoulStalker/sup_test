from datetime import datetime, timedelta

from django.db import models

from .choice_classes import InviteChoices


def ten_days_from_now():
    return datetime.now() + timedelta(days=7)


class Invite(models.Model):
    """
    Модель приглашения
    """

    link = models.CharField(max_length=255, verbose_name="Ссылка")
    status = models.CharField(
        max_length=30,
        choices=InviteChoices.choices,
        default=InviteChoices.ACTIVE,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    expires_at = models.DateTimeField(default=ten_days_from_now, verbose_name="Дата до которой валидна")

    class Meta:
        db_table = "invite"
        verbose_name = "Приглашение"
        verbose_name_plural = "Приглашения"
        app_label = "invites"

    def __str__(self):
        return self.link
