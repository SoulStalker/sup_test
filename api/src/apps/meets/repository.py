"""
Импортируется репозиторий из домена и преобразуется джанговский qureryset в dto
"""

from abc import ABC

from django.shortcuts import get_object_or_404

from src.domain.meet.dtos import MeetDTO, CategoryObject, ParticipantStatusDTO
from src.models.meets import Meet, Category, MeetParticipant

from src.domain.meet.repository import IMeetRepository, ICategoryRepository


class MeetsRepository(IMeetRepository, ABC):
    model = Meet

    def _meet_orm_to_dto(self, meet: Meet) -> MeetDTO:
        return MeetDTO(
            category_id=meet.category.id,
            title=meet.title,
            start_time=meet.start_time,
            author_id=meet.author.id,
            responsible_id=meet.responsible.id,
            participant_statuses=meet.participants,
        )

    def _status_orm_to_dto(
        self, participant_status: MeetParticipant
    ) -> ParticipantStatusDTO:
        return ParticipantStatusDTO(
            participant_id=participant_status.custom_user.id,
            status=participant_status.status,
        )

    def create(self, dto: MeetDTO) -> MeetDTO:
        model = self.model(
            title=dto.title,
            category_id=dto.category_id,
            start_time=dto.start_time,
            author_id=dto.author_id,
            responsible_id=dto.responsible_id,
        )

        model.save()

        # Проставление статусов участников
        self.set_participant_statuses(dto.participant_statuses, model.id)
        return self._meet_orm_to_dto(model)

    def update(self, meet_id: int, dto: MeetDTO) -> MeetDTO:
        Meet.objects.filter(id=meet_id).update(
            title=dto.title,
            category_id=dto.category_id,
            start_time=dto.start_time,
            author_id=dto.author_id,
            responsible_id=dto.responsible_id,
        )
        self.set_participant_statuses(dto.participant_statuses, meet_id)

        meet = Meet.objects.get(id=meet_id)
        return self._meet_orm_to_dto(meet)

    def delete(self, meet_id: int) -> None:
        meet = get_object_or_404(Meet, id=meet_id)
        meet.delete()

    def get_meet_by_id(self, meet_id: int):
        return self._meet_orm_to_dto(Meet.objects.get(id=meet_id))

    def get_meets_list(self) -> list[Meet]:
        return list(Meet.objects.select_related("category").order_by("-start_time"))

    def get_meets_by_category(self, category_id: int) -> list[Meet]:
        return [meet for meet in Meet.objects.filter(category_id=category_id)]

    def set_participant_statuses(
        self, participant_statuses: dict, meet_id: int
    ) -> None:
        """
        Метод проставления статусов участников для мита.
        Если участник уже существует — обновляем статус, если нет — создаем новую запись.
        """
        for user_id, status in participant_statuses.items():
            # Проверяем, существует ли участник в данном мите
            participant, created = MeetParticipant.objects.update_or_create(
                meet_id=meet_id,
                custom_user_id=user_id,
                defaults={"status": status},
                # Обновляем статус, если запись уже существует
            )
            if not created:
                # Если запись не была создана, но была обновлена, просто продолжаем
                continue

    def get_participants_statuses(self, meet_id):
        statuses = MeetParticipant.objects.filter(meet_id=meet_id)
        return [self._status_orm_to_dto(status) for status in statuses]


class CategoryRepository(ICategoryRepository, ABC):
    model = Category

    def _orm_to_dto(self, category: Category) -> CategoryObject:
        return CategoryObject(pk=category.id, name=category.name)

    def create(self, category_name: str) -> CategoryObject:
        category = Category.objects.create(name=category_name)
        return self._orm_to_dto(category)

    def update(self, category_id: int, dto: CategoryObject) -> CategoryObject:
        category = CategoryRepository.get_category_by_id(category_id)
        category.name = dto.name
        return category

    def delete(self, category_id: int) -> None:
        CategoryRepository.get_category_by_id(category_id)

    def get_categories_list(self) -> list[CategoryObject]:
        query = self.model.objects.all()
        return [self._orm_to_dto(category) for category in query]

    def get_category_by_id(self, category_id: int) -> CategoryObject:
        query = self.model.objects.get(id=category_id)
        return self._orm_to_dto(query)
