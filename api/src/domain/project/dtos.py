from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProjectDTO:
    id: int
    name: str
    slug: str
    description: str
    status: str
    participants: dict
    date_created: datetime