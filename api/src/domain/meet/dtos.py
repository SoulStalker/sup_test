from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class CategoryObject:
    """
    ValueObject: Категория мита
    """

    pk: int
    name: str

    def __init__(self, pk: int, name: str) -> None:
        self.pk = pk
        self.name = name


@dataclass
class MeetDTO:
    """
    DTO: Объект мита
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

    PRESENT = "green", "PRESENT"
    ABSENT = "red", "ABSENT"
    WARNED = "yellow", "WARNED"

    def __init__(self, status: str) -> None:
        if status not in [self.PRESENT, self.ABSENT, self.WARNED]:
            raise ValueError(f"Invalid status: {status}")
        self.status = status

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
