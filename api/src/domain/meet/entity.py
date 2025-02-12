from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from src.domain.base import Entity


@dataclass
class CategoryEntity(Entity):
    """
    Сущность категории мита.

    :param name: Название категории.
    """

    name: str

    def verify_data(self) -> Optional[str]:
        """
        Проверяет валидность данных категории.

        :return: Сообщение об ошибке, если данные невалидны, иначе None.
        """
        return super().verify_data(self.name)


@dataclass
class MeetEntity(Entity):
    """
    Сущность мита.

    :param category_id: Идентификатор категории мита.
    :param title: Название мита.
    :param start_time: Время начала мита.
    :param author_id: Идентификатор автора мита.
    :param responsible_id: Идентификатор ответственного за мит.
    :param participant_statuses: Статусы участников мита.
    """

    category_id: int
    title: str
    start_time: datetime
    author_id: int
    responsible_id: int
    participant_statuses: Dict[int, str]

    def verify_data(self) -> Optional[str]:
        """
        Проверяет валидность данных мита.

        :return: Сообщение об ошибке, если данные невалидны, иначе None.
        """
        return super().verify_data(self.title)
