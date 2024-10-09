from dataclasses import dataclass
from datetime import datetime


@dataclass
class CategoryDTO:
    # очень простой объект может здесь не нужен ДТО?
    id: int
    name: str


@dataclass
class MeetDTO:
    category_id: int
    title: str
    start_time: datetime
    author_id: int
    responsible_id: int
    participants_ids: list[int]

