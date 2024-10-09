"""
Импортируется репозиторий из домена и преобразуется джанговский qureryset в нужную сущность (entity или dto)
"""
from abc import ABC

from src.domain.meet.dtos import MeetDTO
from src.models.meets import Meet, Category

from api.src.domain.meet.repository import IMeetRepository


class MeetsRepository(IMeetRepository, ABC):
    def _orm_to_dto(self, meet: Meet) -> MeetDTO:
        return MeetDTO(
            category_id=meet.category.id,
            title=meet.title,
            start_time=meet.start_time,
            author_id=meet.author.id,
            responsible_id=meet.responsible.id,
            participants_ids=meet.participants.all()
            #  под вопросом последняя строка
        )

    def create(self, meet: Meet) -> MeetDTO:
        repository = IMeetRepository()
        meet = repository.create(meet)
        return self._orm_to_dto(meet)

    def update(self, meet_id: int) -> MeetDTO:
        repository = IMeetRepository()
        meet = Meet.get(id=meet_id)
