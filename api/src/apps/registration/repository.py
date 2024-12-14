import os
from abc import ABC

from django.contrib.auth.models import make_password
from django.shortcuts import get_object_or_404
from src.domain.registration.dtos import RegistrationDTO
from src.domain.registration.repository import IRegistrationRepository
from src.domain.user.entity import CreateUserEntity
from src.models.invites import Invite
from src.models.models import CustomUser


class RegistarionRepository(IRegistrationRepository, ABC):
    model = CustomUser

    def create(self, dto: CreateUserEntity) -> RegistrationDTO:
        model = CustomUser.objects.create(
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            password=make_password(dto.password1),
            tg_name=dto.tg_name,
            tg_nickname=dto.tg_nickname,
            google_meet_nickname=dto.google_meet_nickname,
            gitlab_nickname=dto.gitlab_nickname,
            github_nickname=dto.github_nickname,
            role_id=dto.role_id,
            team_id=dto.team_id,
        )
        model.save()

    def chek_invitation_code_or_404(self, invitation_code):
        link = f"{os.getenv('FRONTEND_URL')}/registration/{invitation_code}"
        get_object_or_404(Invite, link=link, status="Активна")
