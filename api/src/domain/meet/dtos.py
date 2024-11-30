from dataclasses import dataclass
from datetime import datetime


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

    id: int
    category_id: int
    title: str
    start_time: datetime
    author_id: int
    responsible_id: int
    participant_statuses: dict


class StatusObject:
    """
    ValueObject: Статусы участников мита
    """

    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    WARNED = "WARNED"

    _descriptions = {
        PRESENT: "Присутствует",
        ABSENT: "Отсутствует",
        WARNED: "Предупредил",
    }

    _colors = {PRESENT: "green", ABSENT: "red", WARNED: "yellow"}

    def __init__(self, status: str) -> None:
        if status not in [self.PRESENT, self.ABSENT, self.WARNED]:
            raise ValueError(f"Invalid status: {status}")
        self.status = status

    def description(self) -> str:
        return self._descriptions[self.status]

    def color(self) -> str:
        return self._colors[self.status]

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
