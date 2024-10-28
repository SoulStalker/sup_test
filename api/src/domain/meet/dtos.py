from dataclasses import dataclass
from datetime import datetime

from src.domain.validators.validators import DataVerifier


class CategoryObject:
    """
    ValueObject: Категория мита
    """

    pk: int
    name: str

    def __init__(self, pk: int, name: str):
        self.pk = pk
        self.name = name

    def verify_data(self):
        letters_error = DataVerifier.verify_letters_only(self.name)
        len_error = DataVerifier.verify_max_value(self.name, 20)
        if letters_error:
            return letters_error
        elif len_error:
            return len_error

@dataclass
class MeetDTO:
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
        if isinstance(other, StatusObject):
            return self.status == other.status
        return False

    def __repr__(self):
        return f"Status(status='{self.status}')"


@dataclass
class ParticipantStatusDTO:
    participant_id: int
    status: StatusObject
