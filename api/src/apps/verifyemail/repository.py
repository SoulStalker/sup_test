import os
import random
from abc import ABC
from datetime import timedelta

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from src.domain.verifyemail.dtos import VerifyEmailDTO
from src.domain.verifyemail.repository import IVerifyemailRepository
from src.models.models import CustomUser
from src.models.verifyemail import VerifyEmail
from src.services.tasks import send_email_to_user


class VerifyemailRepository(IVerifyemailRepository, ABC):
    model = VerifyEmail

    def _invite_orm_to_dto(self, model) -> VerifyEmailDTO:
        return VerifyEmailDTO(
            pk=model.id,
            link=model.link,
            email=model.email,
            created_at=model.created_at,
            expires_at=model.expires_at,
        )

    def create(self, email, name) -> VerifyEmailDTO:
        random_int = random.randint(0000, 9999)
        link = f"{os.getenv('FRONTEND_URL')}/verifyemail/{random_int}"
        created_at = timezone.now()
        expires_at = created_at + timedelta(minutes=60)

        model = self.model(
            link=link,
            email=email,
            created_at=created_at,
            expires_at=expires_at,
        )
        send_email_to_user.delay(name=name, email=email, link=link)
        model.save()
        return self._invite_orm_to_dto(model)

    def chek_verify_code_or_404(self, code):
        """
        Проверяем существует ли ссылка в БД,
        меняем статус юзера на активный,
        удаляем ссылку подтверждения почты из БД
        """
        link = f'{os.getenv('FRONTEND_URL')}/verifyemail/{code}'
        email_user = get_object_or_404(self.model, link=link)
        user = get_object_or_404(CustomUser, email=email_user.email)

        user.is_active = True
        user.save()
        email_user.delete()