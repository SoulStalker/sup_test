"""
Импортируется репозиторий из домена и преобразуется джанговский qureryset в нужную сущность (entity или dto)
"""
from abc import ABC

from src.domain.meet.dtos import MeetDTO
from src.models.meets import Meet, Category

from api.src.domain.meet.repository import IMeetRepository


class MeetsRepository(IMeetRepository, ABC):
    def _orm_to_dto(meet: Meet) -> MeetDTO:
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

    def delete(self, meet_id: int) -> None:
        repository = IMeetRepository()
        repository.delete(meet_id)

    def get_meets_list(self) -> list[MeetDTO]:
        repository = IMeetRepository()
        return repository.get_meets_list()

    def get_meet_by_id(self, meet_id: int) -> MeetDTO:
        repository = IMeetRepository()
        return repository.get_meet_by_id(meet_id)

    def get_meets_by_category(self, category_id: int):
        repository = IMeetRepository()
        return repository.get_meets_by_category(category_id)


class CategoryRepository(IMeetRepository, ABC):
    def create(self, category_name: str) -> MeetDTO:
        repository = IMeetRepository()
        meet = repository.create(category_name)
        return meet

    def update(self, category_id: int) -> MeetDTO:
        repository = IMeetRepository()
        meet = repository.update(category_id)
        return meet

    def delete(self, category_id: int) -> None:
        repository = IMeetRepository()
        repository.delete(category_id)

    def get_meets_list(self) -> list[MeetDTO]:
        repository = IMeetRepository()
        return repository.get_meets_list()

    def get_meet_by_id(self, category_id: int) -> MeetDTO:
        repository = IMeetRepository()
        return repository.get_meet_by_id(category_id)


