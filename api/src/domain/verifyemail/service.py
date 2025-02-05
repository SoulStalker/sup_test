from src.domain.invites.repository import IInviteRepository


class VerifyemailService:
    def __init__(self, repository: IInviteRepository):
        self.__repository = repository

    def create(self, email, name):
        return self.__repository.create(email, name)

    def chek_verify_code_or_404(self, code):
        return self.__repository.chek_verify_code_or_404(code)
