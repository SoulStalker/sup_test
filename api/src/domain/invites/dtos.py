from dataclasses import dataclass
from datetime import datetime


@dataclass
class InviteDTO:
    link: str
    status: str
    created_at: datetime
    expires_at: datetime

    def verify_data(self):
        pass
