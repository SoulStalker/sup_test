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

@dataclass
class TaskDTO:
    id: int
    name: str
    slug: str
    description: str
    status: str
    date_execution: datetime