from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.core.files import File


@dataclass
class CreateTaskDTO:
    """
    DTO для создания задачи.

    :param name: Название задачи.
    :param priority: Приоритет задачи.
    :param tags: Список тегов задачи.
    :param contributor_id: Идентификатор участника, создавшего задачу.
    :param responsible_id: Идентификатор ответственного за задачу.
    :param status: Статус задачи.
    :param closed_at: Дата и время закрытия задачи.
    :param feature_id: Идентификатор фичи, к которой относится задача.
    :param description: Описание задачи.
    """

    name: str
    priority: int
    tags: list[str]
    contributor_id: int
    responsible_id: int
    status: str
    closed_at: Optional[datetime]
    feature_id: int
    description: str


@dataclass
class TaskDTO(CreateTaskDTO):
    """
    DTO для задачи.

    :param id: Уникальный идентификатор задачи.
    :param created_at: Дата и время создания задачи.
    """

    id: int
    created_at: Optional[datetime]


@dataclass
class ProjectDTO:
    """
    DTO для проекта.

    :param name: Название проекта.
    :param logo: Логотип проекта.
    :param description: Описание проекта.
    :param status: Статус проекта.
    :param participants: Список участников проекта.
    :param date_created: Дата и время создания проекта.
    :param responsible_id: Идентификатор ответственного за проект.
    :param slug: Уникальный идентификатор проекта (опционально).
    """

    name: str
    logo: Optional[File]
    description: str
    status: str
    participants: list[int]
    date_created: datetime
    responsible_id: int
    slug: Optional[str] = None


class StatusObject:
    """
    ValueObject: Статусы проекта.

    :param DISCUSSION: Статус "В обсуждении".
    :param DEVELOPMENT: Статус "В разработке".
    :param SUPPORT: Статус "В поддержке".
    """

    DISCUSSION = "В обсуждении"
    DEVELOPMENT = "В разработке"
    SUPPORT = "В поддержке"

    @classmethod
    def choices(cls) -> list[tuple]:
        """
        Возвращает все доступные статусы в виде списка кортежей.

        :return: Список кортежей (статус, статус).
        """
        return [
            (cls.DISCUSSION, cls.DISCUSSION),
            (cls.DEVELOPMENT, cls.DEVELOPMENT),
            (cls.SUPPORT, cls.SUPPORT),
        ]

    def __init__(self, status: str) -> None:
        """
        Инициализирует объект статуса.

        :param status: Статус проекта.
        :raises ValueError: Если статус недопустим.
        """
        if status not in self.get_valid_statuses():
            raise ValueError(f"Invalid status: {status}")
        self.status = status

    @classmethod
    def get_valid_statuses(cls) -> list[str]:
        """
        Возвращает все допустимые статусы.

        :return: Список допустимых статусов.
        """
        return [cls.DISCUSSION, cls.DEVELOPMENT, cls.SUPPORT]

    def __str__(self):
        """
        Возвращает строковое представление статуса.

        :return: Строковое представление статуса.
        """
        return self.status

    def __repr__(self):
        """
        Возвращает строковое представление объекта статуса.

        :return: Строковое представление объекта статуса.
        """
        return f"StatusObject(status='{self.status}')"


@dataclass
class CreateFeaturesDTO:
    """
    DTO для создания фичи.

    :param name: Название фичи.
    :param description: Описание фичи.
    :param importance: Важность фичи.
    :param tags: Список тегов фичи.
    :param participants: Список участников фичи.
    :param responsible_id: Идентификатор ответственного за фичу.
    :param project_id: Идентификатор проекта, к которому относится фича.
    :param status: Статус фичи.
    """

    name: str
    description: str
    importance: int
    tags: list[str]
    participants: list[int]
    responsible_id: int
    project_id: int
    status: str


@dataclass
class FeaturesDTO(CreateFeaturesDTO):
    """
    DTO для фичи.

    :param id: Уникальный идентификатор фичи.
    """

    id: int


class FeaturesChoicesObject:
    """
    ValueObject: Статусы фичи.

    :param NEW: Статус "Новая".
    :param DEVELOPMENT: Статус "Разработка".
    :param TESTING: Статус "Тестирование".
    :param SUCCESS: Статус "Готов".
    """

    NEW = "Новая"
    DEVELOPMENT = "Разработка"
    TESTING = "Тестирование"
    SUCCESS = "Готов"

    @classmethod
    def choices(cls) -> list[tuple]:
        """
        Возвращает все доступные статусы в виде списка кортежей.

        :return: Список кортежей (статус, статус).
        """
        return [
            (cls.NEW, cls.NEW),
            (cls.DEVELOPMENT, cls.DEVELOPMENT),
            (cls.TESTING, cls.TESTING),
            (cls.SUCCESS, cls.SUCCESS),
        ]

    def __init__(self, status: str) -> None:
        """
        Инициализирует объект статуса.

        :param status: Статус фичи.
        :raises ValueError: Если статус недопустим.
        """
        if status not in self.get_valid_statuses():
            raise ValueError(f"Invalid status: {status}")
        self.status = status

    @classmethod
    def get_valid_statuses(cls) -> list[str]:
        """
        Возвращает все допустимые статусы.

        :return: Список допустимых статусов.
        """
        return [cls.NEW, cls.DEVELOPMENT, cls.TESTING, cls.SUCCESS]

    def __str__(self):
        """
        Возвращает строковое представление статуса.

        :return: Строковое представление статуса.
        """
        return self.status

    def __repr__(self):
        """
        Возвращает строковое представление объекта статуса.

        :return: Строковое представление объекта статуса.
        """
        return f"StatusObject(status='{self.status}')"


class TaskChoicesObject(FeaturesChoicesObject):
    """
    ValueObject: Статусы задачи (наследуется от FeaturesChoicesObject).
    """

    pass


@dataclass
class TagDTO:
    """
    DTO для тега.

    :param id: Уникальный идентификатор тега.
    :param name: Название тега.
    :param color: Цвет тега.
    """

    id: int
    name: str
    color: str


@dataclass
class CommentDTO:
    """
    DTO для комментария.

    :param user_id: Идентификатор пользователя, оставившего комментарий.
    :param comment: Текст комментария.
    :param task_id: Идентификатор задачи, к которой относится комментарий.
    """

    user_id: int
    comment: str
    task_id: int
