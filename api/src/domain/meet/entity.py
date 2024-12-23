from dataclasses import dataclass
from datetime import datetime

from src.domain.base import Entity


@dataclass
class CategoryEntity(Entity):
    """
    Категория
    """

    name: str

    def verify_data(self):
        return super().verify_data(self.name)


@dataclass
class MeetEntity(Entity):
    """
    Мит
    """

    category_id: int
    title: str
    start_time: datetime
    author_id: int
    responsible_id: int
    participant_statuses: dict

    def verify_data(self):
        return super().verify_data(self.title)
