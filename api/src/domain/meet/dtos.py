from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional


class CategoryObject:
    """
    ValueObject: Категория мита.

    :param pk: Уникальный идентификатор категории.
    :param name: Название категории.
    """

    pk: int
    name: str

    def __init__(self, pk: int, name: str) -> None:
        self.pk = pk
        self.name = name


@dataclass
class MeetDTO:
    """
    DTO: Объект мита.

    :param id: Уникальный идентификатор мита.
    :param category_id: Идентификатор категории мита.
    :param title: Название мита.
    :param start_time: Время начала мита.
    :param author_id: Идентификатор автора мита.
    :param responsible_id: Идентификатор ответственного за мит.
    :param participant_statuses: Статусы участников мита.
    """

    id: int | None
    category_id: int
    title: str
    start_time: datetime
    author_id: int
    responsible_id: int
    participant_statuses: dict


class StatusObject(Enum):
    """
    ValueObject: Статусы участников мита
    """

    PRESENT = ["green", "PRESENT"]
    ABSENT = ["red", "ABSENT"]
    WARNED = ["yellow", "WARNED"]

    def description(self) -> str:
        return self.value[1]

    def color(self) -> str:
        return self.value[0]

    def __eq__(self, other) -> bool:
        if isinstance(other, StatusObject):
            return self.status == other.status
        return False

    def __repr__(self):
        return f"Status(status='{self.status}')"


@dataclass
class ParticipantStatusDTO:
    """
    DTO: Статус участника мита
    """

    participant_id: int
    status: StatusObject
