from src.domain.registration.dtos import RegistrationDTO
from src.domain.registration.repository import IRegistrationRepository
from src.domain.registration.entity import CreateRegistationEntity



class RegistrationService:
    def __init__(self, repository: IRegistrationRepository):
        self.__repository = repository

    def create(self, dto: CreateRegistationEntity):
        self.__repository.create(dto)

    def chek_invitation_code_or_404(self, invitation_code: str):
        self.__repository.chek_invitation_code_or_404(invitation_code)