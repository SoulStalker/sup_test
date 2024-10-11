from dataclasses import dataclass
from datetime import datetime


@dataclass
class CategoryDTO:
    # очень простой объект может здесь не нужен ДТО?
    id: int
    name: str


@dataclass
class MeetDTO:
    category: CategoryDTO
    title: str
    start_time: datetime
    author_id: int
    responsible_id: int
    participant_statuses: list[dict]

