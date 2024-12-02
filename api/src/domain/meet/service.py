from src.domain.meet.dtos import CategoryObject, MeetDTO
from src.domain.meet.entity import CategoryEntity, MeetEntity
from src.domain.meet.repository import ICategoryRepository, IMeetRepository


class MeetService:
    def __init__(
        self,
        repository: IMeetRepository,
        category_repository: ICategoryRepository,
    ):
        self.__repository = repository
        self.__category_repository = category_repository

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

    def delete(self, pk):
        self.__repository.delete(pk)

    def get_meets_list(self) -> list[MeetDTO]:
        return self.__repository.get_meets_list()

    def get_meet(self, pk) -> MeetDTO:
        return self.__repository.get_meet_by_id(pk)

    def get_meets_by_category(self, dto) -> list[MeetDTO]:
        return self.__repository.get_meets_by_category(dto)

    def set_participants_statuses(self, participant_statuses, meet_id: int):
        return self.__repository.set_participant_statuses(participant_statuses, meet_id)

    def get_participants_statuses(self, meet_id: int):
        return self.__repository.get_participants_statuses(meet_id)


class MeetCategoryService:
    def __init__(self, repository):
        self.__repository = repository

    def create(self, category_name):
        category = CategoryEntity(name=category_name)
        err = category.verify_data()
        if err:
            return None, err
        result = self.__repository.create(category_name)
        return result, None

    def update(self, pk):
        self.__repository.update(pk)

    def delete(self, pk):
        self.__repository.delete(pk)

    def get_categories_list(self) -> list[CategoryObject]:
        return self.__repository.get_categories_list()

    def get_category(self, pk) -> CategoryObject:
        return self.__repository.get_category(pk)
