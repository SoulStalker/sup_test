from dataclasses import dataclass
from datetime import datetime


@dataclass
class InviteDTO:
    pk: int
    link: str
    status: str
    created_at: datetime
    expires_at: datetime
