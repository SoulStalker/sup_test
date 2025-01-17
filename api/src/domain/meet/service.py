# from src.domain.authorization import AuthorizationService
from src.domain.base import BaseService

from .dtos import CategoryObject, MeetDTO
from .entity import CategoryEntity, MeetEntity
from .repository import ICategoryRepository, IMeetRepository


class MeetService(BaseService):
    def __init__(
        self,
        repository: IMeetRepository,
        category_repository: ICategoryRepository,
    ):
        self._repository = repository
        self.__category_repository = category_repository

    def create(self, dto, user_id):
        """
        Создание мита с проверкой прав пользователя.
        """
        entity = MeetEntity(
            dto.category_id,
            dto.title,
            dto.start_time,
            dto.author_id,
            dto.responsible_id,
            dto.participant_statuses,
        )
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(self, pk, dto, user_id):
        """
        Обновление мита с проверкой прав пользователя.
        """

        entity = MeetEntity(
            category_id=dto.category_id,
            title=dto.title,
            start_time=dto.start_time,
            author_id=dto.author_id,
            responsible_id=dto.responsible_id,
            participant_statuses=dto.participant_statuses,
        )
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def get_meets_by_category(self, dto, user_id) -> list[MeetDTO]:
        """
        Получение митов по категории с проверкой прав пользователя.
        """
        return self._repository.get_meets_by_category(dto)

    def get_participants_statuses(self, meet_id: int):
        return self._repository.get_participants_statuses(meet_id)

    def set_participants_statuses(self, participant_statuses, meet_id: int):
        return self._repository.set_participant_statuses(
            participant_statuses, meet_id
        )

    def has_permission(self, user_id: int, action: str, obj=None) -> bool:
        """
        Проверка наличия разрешения у пользователя.
        - action: код действия, например, "EDIT_TASK".
        - obj: объект, для которого проверяется разрешение. Если None, проверяется глобальное разрешение.
        """
        return self.has_permission(user_id, action, obj)

    # def get_by_id(self, pk, user_id):
    #     # Проверяем наличие прав
    #     model = self._repository.get_by_id(pk, user_id)
    #     if not self._repository.has_permission(user_id, "EDIT", model):
    #         return None, "У вас нет прав на просмотр данного объекта"
    #     return self._repository.get_by_id(pk, user_id)


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
