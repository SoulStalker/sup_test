from dataclasses import dataclass
from datetime import datetime
from src.domain.validators.validators import DataVerifier


@dataclass
class ProjectEntity:
    id: int
    name: str
    slug: str
    description: str
    status: str
    participants: dict
    date_created: datetime

    def verify_data(self):
        return DataVerifier.verify_max_value(self.name, 100)