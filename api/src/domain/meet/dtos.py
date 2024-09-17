from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True)
class Category:
    name: str


@dataclass(frozen=True)
class Meet:
    category: int
    title: str
    start_date: date
    start_time: time
    author: str
    responsible: str
    participants: list[str]