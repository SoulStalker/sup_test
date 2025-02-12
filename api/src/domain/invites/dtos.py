from dataclasses import dataclass
from datetime import datetime


@dataclass
class InviteDTO:
    """
    DTO (Data Transfer Object) для передачи данных о приглашении.

    :param id: Уникальный идентификатор приглашения.
    :param link: Ссылка на приглашение.
    :param status: Статус приглашения.
    :param created_at: Дата и время создания приглашения.
    :param expires_at: Дата и время истечения срока действия приглашения.
    """

    id: int
    link: str
    status: str
    created_at: datetime
    expires_at: datetime
