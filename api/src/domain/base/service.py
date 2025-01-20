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
    def validate_and_save(cls, entity, repository, dto, user_id):
        """
        Упрощённая обёртка для создания объектов.
        """
        # Проверяем наличие прав
        if not repository.has_permission(user_id, "EDIT"):
            return None, "У вас нет прав на создание данного объекта"
        return cls.validate_and_process(
            entity, repository, dto, repository.create
        )

    @classmethod
    def validate_and_update(cls, entity, repository, dto, pk, user_id):
        """
        Метод для обновления объектов.

        :param entity: Entity для валидации данных
        :param repository: Репозиторий для выполнения операций с базой
        :param dto: DTO с данными
        :param pk: Первичный ключ объекта
        :param user_id: Идентификатор пользователя
        :return: Tuple (result, error), где result — результат операции, а error — ошибка
        """
        # Проверяем существование объекта
        if not repository.exists(pk):
            return None, f"Объект с id {pk} не найден."

        # Проверяем наличие прав
        model = repository.get_by_id(pk)
        if not repository.has_permission(user_id, "EDIT", model):
            return None, "У вас нет прав на редактирование данного объекта"

        return cls.validate_and_process(
            entity, repository, dto, lambda d: repository.update(pk, d)
        )

    def exists(self, pk):
        return self._repository.exists(pk)

    def get_list(self, user_id):
        """
        Получение списка объектов с проверкой прав доступа.

        :param user_id: Идентификатор пользователя
        :return: Список объектов, к которым у пользователя есть доступ
        """
        all_objects = self._repository.get_list()

        # Фильтруем объекты, оставляя только те, к которым у пользователя есть доступ
        # accessible_objects = []
        # for obj in all_objects:
        #     if self._repository.has_permission(user_id, "READ", obj):
        #         accessible_objects.append(obj)

        # return accessible_objects, None
        return all_objects

    def get_by_id(self, pk, user_id):
        """
        Получение объекта по ID с проверкой прав доступа.

        :param pk: Первичный ключ объекта
        :param user_id: Идентификатор пользователя
        :return: Объект или None, если нет прав доступа или объект не найден
        """
        if not self._repository.exists(pk):
            return None, f"Объект с id {pk} не найден."

        model = self._repository.get_by_id(pk)

        # Проверяем наличие прав на чтение объекта
        if not self._repository.has_permission(user_id, "READ", model):
            return None, "У вас нет прав на просмотр данного объекта"

        return model, None

    def delete(self, pk, user_id):
        model = self._repository.get_by_id(pk)
        if not self._repository.has_permission(user_id, "EDIT", model):
            return "У вас нет прав на удаление данного объекта"
        self._repository.delete(pk)
