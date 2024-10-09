from src.domain.meet.dtos import CategoryDTO, MeetDTO


class MeetService:
    def __init__(self, repository):
        self.__repository = repository

    def create(self, dto):
        self.__repository.create(dto)

    def update(self, pk):
        self.__repository.update(pk)

    def delete(self, pk):
        self.__repository.delete(pk)

    def get_meets_list(self) -> list[MeetDTO]:
        pass

    def get_meet(self, pk) -> MeetDTO:
        pass

    def get_meets_by_category(self, category) -> list[MeetDTO]:
        pass


class MeetCategoryService:
    def __init__(self, repository):
        self.__repository = repository

    def create(self, dto):
        self.__repository.create(dto)

    def update(self, pk):
        self.__repository.update(pk)

    def delete(self, pk):
        self.__repository.delete(pk)

    def get_list(self) -> list[CategoryDTO]:
        return self.__repository.get_list()

    def get_category(self, pk) -> CategoryDTO:
        return self.__repository.get_category(pk)
