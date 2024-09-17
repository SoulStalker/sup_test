"""
Импортируется репозиторий из домена и преобразуется джанговский qureryset в нужную сущность (entity или dto)
"""

from domain.repository import IMeetRepository

class MeetsRepository(IMeetRepository):
    pass


