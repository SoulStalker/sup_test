from dataclasses import dataclass
from datetime import datetime
from src.domain.validators.validators import DataVerifier


class CategoryObject:
    """
    ValueObject: Категория мита
    """

    def __init__(self, pk: int, name: str):
        self.pk = pk
        self.name = name

    pk: int
    name: str


@dataclass
class MeetEntity:
    category_id: int
    title: str
    start_time: datetime
    author_id: int
    responsible_id: int
    participant_statuses: dict

    def verify_data(self):
        letters_error = DataVerifier.verify_letters_space_only(self.title)
        len_error = DataVerifier.verify_max_value(self.title, 20)
        if letters_error:
            return letters_error
        elif len_error:
            return len_error
