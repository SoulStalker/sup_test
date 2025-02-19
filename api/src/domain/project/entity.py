from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.core.files import File
from src.domain.validators import DataVerifier


@dataclass
class ProjectEntity:
    """
    Сущность проекта.

    :param name: Название проекта.
    :param logo: Логотип проекта.
    :param description: Описание проекта.
    :param status: Статус проекта.
    :param participants: Список участников проекта.
    :param date_created: Дата и время создания проекта.
    :param responsible_id: Идентификатор ответственного за проект.
    """

    name: str
    logo: Optional[File]
    description: str
    status: str
    participants: list[int]
    date_created: datetime
    responsible_id: int

    def verify_data(self) -> Optional[str]:
        """
        Проверяет валидность данных проекта.

        :return: Сообщение об ошибке, если данные невалидны, иначе None.
        """
        return DataVerifier.verify_max_value(self.name, 100)


@dataclass
class FeaturesEntity:
    """
    Сущность фичи.

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

    def verify_data(self) -> Optional[str]:
        """
        Проверяет валидность данных фичи.

        :return: Сообщение об ошибке, если данные невалидны, иначе None.
        """
        return DataVerifier.verify_max_value(self.name, 100)


@dataclass
class TaskEntity:
    """
    Сущность задачи.

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

    def verify_data(self) -> Optional[str]:
        """
        Проверяет валидность данных задачи.

        :return: Сообщение об ошибке, если данные невалидны, иначе None.
        """
        return DataVerifier.verify_max_value(self.name, 100)


@dataclass
class CommentEntity:
    """
    Сущность комментария.

    :param user_id: Идентификатор участника, создавшего комментарий.
    :param comment: Комментарий.
    :param tags: Идентификатор задачи, к которой относится комментарий.
    """

    user_id: int
    comment: str
    task_id: int

    def verify_data(self) -> Optional[str]:
        """
        Проверяет валидность данных задачи.

        :return: Сообщение об ошибке, если данные невалидны, иначе None.
        """
        return DataVerifier.verify_letter_digits_symbols(self.comment)