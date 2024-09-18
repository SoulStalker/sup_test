"""
Импортируется репозиторий из домена и преобразуется джанговский qureryset в нужную сущность (entity или dto)
"""
from src.models.meets import Meet

from domain.repository import IMeetRepository


class MeetsRepository(IMeetRepository):
    model = Meet

    def create(self, dto: CreateMeetDTO):
        model = self.model(**dto.dict())
        model.save()
