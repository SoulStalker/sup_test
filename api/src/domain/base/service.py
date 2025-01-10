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

        return cls.validate_and_process(
            entity, repository, dto, lambda d: repository.update(pk, d)
        )

    def exists(self, pk):
        return self._repository.exists(pk)

    def get_list(self) -> list:
        return self._repository.get_list()

    def get_by_id(self, pk):
        return self._repository.get_by_id(pk)

    def delete(self, pk) -> None:
        self._repository.delete(pk)

    def orm_to_dto(
        orm_instance, dto_class, field_mapping=None, custom_handlers=None
    ):
        """
        Преобразует ORM-модель в DTO-объект.

        :param orm_instance: экземпляр модели ORM.
        :param dto_class: класс DTO.
        :param field_mapping: словарь, где ключи — поля ORM, значения — атрибуты DTO.
        :param custom_handlers: словарь, где ключи — атрибуты DTO, значения — функции для их вычисления.
        :return: экземпляр DTO.
        """
        field_mapping = field_mapping or {}
        custom_handlers = custom_handlers or {}

        # Получаем атрибуты DTO
        dto_data = {}

        for field in dto_class.__annotations__:  # Аннотации из dataclass
            if field in custom_handlers:
                # Если есть кастомный обработчик
                dto_data[field] = custom_handlers[field](orm_instance)
            elif field in field_mapping:
                # Если поле указано в field_mapping
                dto_data[field] = getattr(
                    orm_instance, field_mapping[field], None
                )
            else:
                # По умолчанию ищем атрибут с тем же названием
                dto_data[field] = getattr(orm_instance, field, None)

        return dto_class(**dto_data)
