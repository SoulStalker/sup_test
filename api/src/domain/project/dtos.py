from dataclasses import dataclass
from datetime import datetime

from django.core.files import File


@dataclass
class CreateTaskDTO:
    name: str
    priority: int
    tags: list
    contributor_id: int
    responsible_id: int
    status: str
    closed_at: datetime | None
    feature_id: int
    description: str


@dataclass
class TaskDTO(CreateTaskDTO):
    id: int
    created_at: datetime


@dataclass
class ProjectDTO:
    name: str
    logo: File | None
    description: str
    status: str
    participants: list
    date_created: datetime
    responsible_id: int
    slug: str = None


class StatusObject:
    """ValueObject: Статусы проекта"""

    DISCUSSION = "В обсуждении"
    DEVELOPMENT = "В разработке"
    SUPPORT = "В поддержке"

    @classmethod
    def choices(cls) -> list:
        """Возвращает все доступные статусы в виде списка кортежей."""
        return [
            (cls.DISCUSSION, cls.DISCUSSION),
            (cls.DEVELOPMENT, cls.DEVELOPMENT),
            (cls.SUPPORT, cls.SUPPORT),
        ]

    def __init__(self, status: str) -> None:
        if status not in self.get_valid_statuses():
            raise ValueError(f"Invalid status: {status}")
        self.status = status

    @classmethod
    def get_valid_statuses(cls) -> list:
        """Возвращает все допустимые статусы."""
        return [cls.DISCUSSION, cls.DEVELOPMENT, cls.SUPPORT]

    def __str__(self):
        return self.status

    def __repr__(self):
        return f"StatusObject(status='{self.status}')"


@dataclass
class FeaturesDTO:
    name: str
    description: str
    importance: int
    tags: list
    participants: list
    responsible_id: int
    project_id: int
    status: str


class FeaturesChoicesObject:
    NEW = "Новая"
    DEVELOPMENT = "Разработка"
    TESTING = "Тестирование"
    SUCCESS = "Готов"

    @classmethod
    def choices(cls):
        return [
            (cls.NEW, cls.NEW),
            (cls.DEVELOPMENT, cls.DEVELOPMENT),
            (cls.TESTING, cls.TESTING),
            (cls.SUCCESS, cls.SUCCESS),
        ]

    def __init__(self, status: str):
        if status not in self.get_valid_statuses():
            raise ValueError(f"Invalid status: {status}")
        self.status = status

    @classmethod
    def get_valid_statuses(cls) -> list:
        return [cls.NEW, cls.DEVELOPMENT, cls.TESTING, cls.SUCCESS]

    def __str__(self):
        return self.status

    def __repr__(self):
        return f"StatusObject(status='{self.status}')"


class TaskChoicesObject(FeaturesChoicesObject):
    pass
