from src.domain.meet.dtos import CategoryDTO


class MeetService:
    def __init__(self, repository):
        self.__repository = repository

    def create(self, dto):
        self.__repository.create(dto)

    def delete(self, pk):
        self.__repository.delete(pk)

    def get_list(self):
        pass


class CategoryMeetService:
    def __init__(self, repository):
        self.__repository = repository

    def create(self, dto):
        self.__repository.create(dto)

    def delete(self, pk):
        self.__repository.delete(pk)

    def get_list(self) -> list[CategoryDTO]:
        return self.__repository.get_list()


