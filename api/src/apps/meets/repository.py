"""
Импортируется репозиторий из домена и преобразуется джанговский qureryset в нужную сущность (entity или dto)
"""
from src.models.meets import Meet

from api.src.domain.meet.repository import IMeetRepository


class MeetsRepository(IMeetRepository):
    pass

    # def create(self, dto: CreateMeetDTO):
    #     model = self.model(**dto.dict())
    #     model.save()
