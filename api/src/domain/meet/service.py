from src.domain.base import BaseService
from src.domain.meet.dtos import CategoryObject, MeetDTO
from src.domain.meet.entity import CategoryEntity, MeetEntity
from src.domain.meet.repository import ICategoryRepository, IMeetRepository


class MeetService(BaseService):
    def __init__(
        self,
        repository: IMeetRepository,
        category_repository: ICategoryRepository,
    ):
        self._repository = repository
        self.__category_repository = category_repository

    def create(self, dto):
        """
        Создание мита
        """
        entity = MeetEntity(
            dto.category_id,
            dto.title,
            dto.start_time,
            dto.author_id,
            dto.responsible_id,
            dto.participant_statuses,
        )
        return self.validate_and_save(entity, self._repository, dto)

    def update(self, pk, dto):
        entity = MeetEntity(
            category_id=dto.category_id,
            title=dto.title,
            start_time=dto.start_time,
            author_id=dto.author_id,
            responsible_id=dto.responsible_id,
            participant_statuses=dto.participant_statuses,
        )
        return self.validate_and_update(entity, self._repository, dto, pk)

    def get_meets_by_category(self, dto) -> list[MeetDTO]:
        return self._repository.get_meets_by_category(dto)

    def get_participants_statuses(self, meet_id: int):
        return self._repository.get_participants_statuses(meet_id)

    def set_participants_statuses(self, participant_statuses, meet_id: int):
        return self._repository.set_participant_statuses(
            participant_statuses, meet_id
        )


class MeetCategoryService(BaseService):
    def __init__(
        self,
        repository: ICategoryRepository,
    ):
        self._repository = repository

    def create(self, category_name):
        """
        Создание категории
        """

        entity = CategoryEntity(name=category_name)
        dto = CategoryEntity(name=category_name)

        return self.validate_and_save(entity, self._repository, dto)

    def update(self, pk, category_name):
        """
        Обновление категории
        """
        entity = CategoryEntity(name=category_name)
        dto = CategoryObject(name=category_name)
        return self.validate_and_update(entity, self._repository, dto, pk)
