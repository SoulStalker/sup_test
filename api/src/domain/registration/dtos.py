from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegistrationDTO:
    name: str
    surname: str
    email: str
    tg_name: str
    tg_nickname: str
    google_meet_nickname: str
    gitlab_nickname: str
    github_nickname: str
    password1: str
    password2: str
    role_id: int
    team_id: int | None
    permissions_ids: list[int]
    date_joined: datetime | None