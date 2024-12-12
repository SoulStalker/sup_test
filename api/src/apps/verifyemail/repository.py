import os
import random
from abc import ABC
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from src.domain.verifyemail.repository import IVerifyemailRepository
from src.domain.verifyemail.dtos import VerifyEmailDTO
from src.models.verifyemail import VerifyEmail
from src.models.models import CustomUser


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

    def create(self, email) -> VerifyEmailDTO:
        invite_link = f"{os.getenv('FRONTEND_URL')}/verifyemail/{random.randint(0000, 9999)}"
        email = email
        created_at = timezone.now()
        expires_at = created_at + timedelta(minutes=60)

        model = self.model(
            link=invite_link,
            email=email,
            created_at=created_at,
            expires_at=expires_at,
        )
        model.save()
        return self._invite_orm_to_dto(model)

    def chek_verify_code_or_404(self, code):
        """Проверяем существует ли ссылка в БД и меняем статус юзера на активный"""
        link = f'{os.getenv('FRONTEND_URL')}/verifyemail/{code}'
        email_user = get_object_or_404(self.model, link=link).email
        user = get_object_or_404(CustomUser, email=email_user)
        user.is_active = True
        user.save()