"""
Импортируется репозиторий из домена и преобразуется джанговский qureryset в dto
"""

from abc import ABC

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from src.domain.meet.dtos import CategoryObject, MeetDTO, ParticipantStatusDTO
from src.domain.meet.entity import CategoryEntity
from src.domain.meet.repository import ICategoryRepository, IMeetRepository
from src.models.meets import Category, Meet, MeetParticipant

user = get_user_model()


class MeetsRepository(IMeetRepository, ABC):
    model = Meet

    @classmethod
    def exists(cls, pk: int) -> bool:
        return cls.model.objects.filter(id=pk).exists()

    from django.contrib.contenttypes.models import ContentType
    from django.shortcuts import get_object_or_404

    def has_permission(self, user_id: int, action: str, obj=None) -> bool:
        """
        Проверка наличия прав у пользователя на выполнение действия.
        :param user_id: ID пользователя
        :param action: код действия (например, "EDIT", "DELETE")
        :param obj: объект, для которого проверяются права (например, Meet)
        :return: bool
        """
        content_type = ContentType.objects.get_for_model(self.model)
        object_id = obj.id if obj else None

        current_user = get_object_or_404(user, pk=user_id)
        permission = current_user.permissions.filter(
            code=action,
            content_type=content_type,
            object_id=object_id,
        ).exists()

        return permission

    @classmethod
    def _meet_orm_to_dto(cls, meet: Meet) -> MeetDTO:
        return MeetDTO(
            id=meet.id,
            category_id=meet.category.id,
            title=meet.title,
            start_time=meet.start_time,
            author_id=meet.author.id,
            responsible_id=meet.responsible.id,
            participant_statuses={
                participant_status.custom_user.id: participant_status.status
                for participant_status in meet.meetparticipant_set.all()
            },
        )

    @classmethod
    def _status_orm_to_dto(
        cls, participant_status: MeetParticipant
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

    def delete(self, pk: int) -> None:
        meet = get_object_or_404(Meet, id=pk)
        meet.delete()

    def get_by_id(self, meet_id: int):
        return self._meet_orm_to_dto(Meet.objects.get(id=meet_id))

    def get_list(self) -> list[MeetDTO]:
        return [
            self._meet_orm_to_dto(meet)
            for meet in Meet.objects.select_related("category").order_by(
                "-start_time"
            )
        ]

    def get_meets_by_category(self, category_id: int) -> list[MeetDTO]:
        return [
            self._meet_orm_to_dto(meet)
            for meet in Meet.objects.filter(category_id=category_id)
        ]

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

    def create(self, category: CategoryEntity) -> CategoryObject:
        category = Category.objects.create(name=category.name)
        return self._orm_to_dto(category)

    def update(self, category_id: int, dto: CategoryObject) -> CategoryObject:
        category = self.model.objects.filter(pk=category_id)
        category.name = dto.name
        category.save()
        return category

    def delete(self, pk: int) -> None:
        category = self.model.objects.filter(pk=pk)
        category.delete()

    def get_list(self) -> list[CategoryObject]:
        query = self.model.objects.all()
        return [self._orm_to_dto(category) for category in query]

    def get_by_id(self, pk: int) -> CategoryObject:
        query = self.model.objects.get(id=pk)
        return self._orm_to_dto(query)
