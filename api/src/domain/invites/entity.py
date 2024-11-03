from dataclasses import dataclass
from datetime import datetime


@dataclass
class InviteEntity:
    pk: int
    link: str
    status: str
    created_at: datetime
    expires_at: datetime

    def expire_status(self):
        if self.status == "ACTIVE" and self.expires_at < datetime.now():
            self.status = "EXPIRED"
        return self.status

    def use_invite(self):
        self.status = "USED"
