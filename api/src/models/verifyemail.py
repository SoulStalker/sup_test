from django.db import models
from .validators import ModelValidator


class VerifyEmail(models.Model):
    """
    Модель ссылки для подверждения почты
    """

    link = models.CharField(
        max_length=255, verbose_name="Ссылка"
        )
    email = models.EmailField(
        max_length=50,
        unique=True,
        validators=[ModelValidator.validate_email()],
        verbose_name="email",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
        )
    expires_at = models.DateTimeField(
        verbose_name="Дата до которой валидна"
        )
    
    class Meta:
        db_table = "verify_email"
        verbose_name = "Подтверждение почты"
        verbose_name_plural = "Подтверждение почты"

    def __str__(self):
        return self.link
