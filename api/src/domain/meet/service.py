from src.domain.meet.dtos import CategoryDTO, MeetDTO
from src.domain.meet.repository import IMeetRepository, ICategoryRepository


class MeetService:
    def __init__(self, repository: IMeetRepository, category_repository: ICategoryRepository):
        self.__repository = repository
        self.__category_repository = category_repository

    def create(self, dto):
        category = dto.category
        try:
            meet = MeetDTO(category, dto.title, dto.start_time, dto.author_id, dto.responsible_id, dto.participant_statuses)
        except Exception as e:
            raise Exception('Ah shit', e)
        return meet

    def update(self, pk):
        self.__repository.update(pk)

    def delete(self, pk):
        self.__repository.delete(pk)

    def get_meets_list(self) -> list[MeetDTO]:
        return self.__repository.get_meets_list()

    def get_meet(self, pk) -> MeetDTO:
        return self.__repository.get_meet_by_id(pk)

    def get_meets_by_category(self, dto) -> list[MeetDTO]:
        category = self.__category_repository.get_category_by_id(dto.category_id)
        try:
            return [meet for meet in self.__repository.get_meets_by_category(category)]
        except Exception as e:
            raise Exception('Meets not found', e)


class MeetCategoryService:
    def __init__(self, repository):
        self.__repository = repository

    def create(self, dto):
        self.__repository.create(dto)

    def update(self, pk):
        self.__repository.update(pk)

    def delete(self, pk):
        self.__repository.delete(pk)

    def get_categories_list(self) -> list[CategoryDTO]:
        return self.__repository.get_categories_list()

    def get_category(self, pk) -> CategoryDTO:
        return self.__repository.get_category(pk)
