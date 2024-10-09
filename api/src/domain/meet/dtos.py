from dataclasses import dataclass
from datetime import date, time


@dataclass
class CategoryDTO:
    # очень простой объект может нафиг не нужен ДТО?
    id: int
    name: str


@dataclass
class MeetDTO:
    category_id: int
    title: str
    start_date: date
    start_time: time
    # может объединить в дату и время?
    author_id: int
    responsible_id: int
    participants_ids: list[int]


@dataclass
class CreateMeetDTO:
    # может не нужен этот ДТО?
    category: int
    title: str
    start_date: date
    start_time: time
    author: str
    responsible: str
    participants: list[str]
