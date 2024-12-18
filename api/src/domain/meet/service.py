from src.domain.meet.dtos import CategoryObject, MeetDTO
from src.domain.meet.entity import CategoryEntity, MeetEntity
from src.domain.meet.repository import ICategoryRepository, IMeetRepository


class BaseService:
    @classmethod
    def validate_and_process(cls, entity, repository, dto, save_method):
        """
        Универсальный метод для валидации и сохранения/обновления данных.

        :param entity: Entity для валидации данных
        :param repository: Репозиторий для выполнения операций с базой
        :param dto: DTO с данными
        :param save_method: Метод репозитория (например, create или update)
        :return: Tuple (result, error), где result — результат операции, а error — ошибка
        """
        err = entity.verify_data()
        if err:
            return None, err

        result = save_method(dto)
        return result, None

    @classmethod
    def validate_and_save(cls, entity, repository, dto):
        """
        Упрощённая обёртка для создания объектов.
        """
        return cls.validate_and_process(
            entity, repository, dto, repository.create
        )

    @classmethod
    def validate_and_update(cls, entity, repository, dto, pk):
        """
        Метод для обновления объектов.

        :param entity: Entity для валидации данных
        :param repository: Репозиторий для выполнения операций с базой
        :param dto: DTO с данными
        :param pk: Первичный ключ объекта
        :return: Tuple (result, error), где result — результат операции, а error — ошибка
        """
        # Проверяем существование объекта
        if not repository.exists(pk):
            return None, f"Объект с id {pk} не найден."

        # todo что здесь просиходит?
        return cls.validate_and_process(
            entity, repository, dto, lambda d: repository.update(pk, d)
        )

    def get_list(self) -> list:
        return self.__repository.get_list()

    def get_by_id(self, pk):
        return self.__repository.get_by_id(pk)

    def delete(self, pk) -> None:
        self.__repository.delete(pk)


class MeetService(BaseService):
    def __init__(
        self,
        repository: IMeetRepository,
        category_repository: ICategoryRepository,
    ):
        self.__repository = repository
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
        return self.validate_and_save(entity, self.__repository, dto)

    def update(self, pk, dto):
        entity = MeetEntity(
            category_id=dto.category_id,
            title=dto.title,
            start_time=dto.start_time,
            author_id=dto.author_id,
            responsible_id=dto.responsible_id,
            participant_statuses=dto.participant_statuses,
        )
        return self.validate_and_update(entity, self.__repository, dto, pk)

    def get_meets_by_category(self, dto) -> list[MeetDTO]:
        return self.__repository.get_meets_by_category(dto)

    def get_participants_statuses(self, meet_id: int):
        return self.__repository.get_participants_statuses(meet_id)

    def set_participants_statuses(self, participant_statuses, meet_id: int):
        return self.__repository.set_participant_statuses(
            participant_statuses, meet_id
        )


class MeetCategoryService(BaseService):
    def __init__(
        self,
        repository: ICategoryRepository,
    ):
        self.__repository = repository

    def create(self, category_name):
        """
        Создание категории
        """
        entity = CategoryEntity(name=category_name)
        dto = CategoryObject(name=category_name)

        return self.validate_and_save(entity, self.__repository, dto)

    def update(self, pk, category_name):
        """
        Обновление категории
        """
        entity = CategoryEntity(name=category_name)
        dto = CategoryObject(name=category_name)
        return self.validate_and_update(entity, self.__repository, dto, pk)
