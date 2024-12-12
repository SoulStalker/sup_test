from dataclasses import dataclass
from datetime import datetime


@dataclass
class VerifyEmailDTO:
    pk: int
    link: str
    email: str
    created_at: datetime
    expires_at: datetime

    def verify_data(self):
        pass
