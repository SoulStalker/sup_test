from dataclasses import dataclass
from datetime import datetime, timedelta

from src.models.choice_classes import InviteChoices


@dataclass
class InviteEntity:
    pk: int
    link: str
    status: str
    created_at: datetime
    expires_at: datetime

    def expire_status(self):
        if self.status == InviteChoices.ACTIVE and self.created_at.replace(
            tzinfo=None
        ) < datetime.now() - timedelta(days=7):
            self.status = InviteChoices.EXPIRED
        return self.status

    def use_invite(self):
        self.status = InviteChoices.USED
        return self.status
