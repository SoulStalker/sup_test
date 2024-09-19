from dataclasses import dataclass
from datetime import date, time


@dataclass
class CategoryDTO:
    id: int
    name: str


@dataclass
class MeetDTO:
    category: int
    title: str
    start_date: date
    start_time: time
    author: str
    responsible: str
    participants: list[str]


@dataclass
class CreateMeetDTO:
    category: int
    title: str
    start_date: date
    start_time: time
    author: str
    responsible: str
    participants: list[str]
