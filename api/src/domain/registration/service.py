from src.domain.registration.dtos import RegistrationDTO
from src.domain.registration.repository import IRegistrationRepository
from src.domain.registration.entity import RegistationEntity


class RegistrationService:
    def __init__(self, repository: IRegistrationRepository):
        self.__repository = repository

    def create(self, dto: RegistrationDTO):
        registration = RegistationEntity(
            dto.name,
            dto.surname,
            dto.email,
            dto.password1,
            dto.password2,
            dto.tg_name,
            dto.tg_nickname,
            dto.google_meet_nickname,
            dto.gitlab_nickname,
            dto.github_nickname,
        )
        err = registration.verify_data()
        if err:
            return err
        self.__repository.create(dto)

    def chek_invitation_code_or_404(self, invitation_code: str):
        self.__repository.chek_invitation_code_or_404(invitation_code)