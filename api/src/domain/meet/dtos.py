from dataclasses import dataclass
from datetime import datetime


class CategoryObject:
    """
    ValueObject: Category of meet
    """
    def __init__(self, name: str):
        self.name = name

    name: str


@dataclass
class MeetDTO:
    category: CategoryObject
    title: str
    start_time: datetime
    author_id: int
    responsible_id: int
    participant_statuses: list[dict]


class Status:
    """
    ValueObject: Status of the meet
    """
    PRESENT = "present"
    ABSENT = "absent"
    WARNED = "warned"

    _descriptions = {
        PRESENT: "Присутствует",
        ABSENT: "Отсутствует",
        WARNED: "Предупредил"
    }

    _colors = {
        PRESENT: "green",
        ABSENT: "red",
        WARNED: "yellow"
    }

    def __init__(self, status: str):
        if status not in [self.PRESENT, self.ABSENT, self.WARNED]:
            raise ValueError(f"Invalid status: {status}")
        self.status = status

    def description(self):
        return self._descriptions[self.status]

    def color(self):
        return self._colors[self.status]

    def __eq__(self, other):
        if isinstance(other, Status):
            return self.status == other.status
        return False

    def __repr__(self):
        return f"Status(status='{self.status}')"
