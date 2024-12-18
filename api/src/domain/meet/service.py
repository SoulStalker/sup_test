from src.domain.meet.dtos import MeetDTO
from src.domain.meet.entity import CategoryEntity, MeetEntity
from src.domain.meet.repository import ICategoryRepository, IMeetRepository


class BaseService:
    def __init__(
        self,
        repository: IMeetRepository,
        category_repository: ICategoryRepository,
    ):
        self.__repository = repository
        self.__category_repository = category_repository

    def get_list(self) -> list:
        return self.__repository.get_list()

    def get_by_id(self, pk):
        return self.__repository.get_by_id(pk)

    def delete(self, pk) -> None:
        self.__repository.delete(pk)


class MeetService(BaseService):

    def create(self, dto: MeetDTO):
        meet = MeetEntity(
            dto.category_id,
            dto.title,
            dto.start_time,
            dto.author_id,
            dto.responsible_id,
            dto.participant_statuses,
        )
        err = meet.verify_data()
        if err:
            return err
        self.__repository.create(dto)

    def update(self, meet_id, dto):
        meet = MeetEntity(
            dto.category_id,
            dto.title,
            dto.start_time,
            dto.author_id,
            dto.responsible_id,
            dto.participant_statuses,
        )
        err = meet.verify_data()
        if err:
            return err
        self.__repository.update(meet_id, dto)

    def get_meets_by_category(self, dto) -> list[MeetDTO]:
        return self.__repository.get_meets_by_category(dto)

    def get_participants_statuses(self, meet_id: int):
        return self.__repository.get_participants_statuses(meet_id)

    def set_participants_statuses(self, participant_statuses, meet_id: int):
        return self.__repository.set_participant_statuses(
            participant_statuses, meet_id
        )


class MeetCategoryService(BaseService):
    def create(self, category_name):
        category = CategoryEntity(name=category_name)
        err = category.verify_data()
        if err:
            return None, err
        result = self.__repository.create(category_name)
        return result, None

    def update(self, pk):
        self.__repository.update(pk)
