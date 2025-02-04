import factory
from django.utils import timezone
from datetime import timedelta

from src.models.invites import Invite
from src.models.choice_classes import InviteChoices



class InviteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invite

    # Генерация ссылки
    link = factory.LazyFunction(lambda: f"https://example.com/registration/{secrets.token_urlsafe(16)}")

    # Статус по умолчанию
    status = InviteChoices.ACTIVE

    # Дата создания — текущее время
    created_at = factory.LazyFunction(timezone.now)

    # Дата истечения — через 7 дней от created_at
    expires_at = factory.LazyAttribute(lambda o: o.created_at + timedelta(days=7))