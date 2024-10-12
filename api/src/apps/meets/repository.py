"""
Импортируется репозиторий из домена и преобразуется джанговский qureryset в нужную сущность (entity или dto)
"""
from abc import ABC

from django.shortcuts import get_object_or_404

from src.domain.meet.dtos import MeetDTO, CategoryObject, Status
from src.models.meets import Meet, Category, MeetParticipant

from src.domain.meet.repository import IMeetRepository, ICategoryRepository


class MeetsRepository(IMeetRepository, ABC):
    model = Meet

    def _orm_to_dto(meet: Meet) -> MeetDTO:
        return MeetDTO(
            category_id=meet.category.id,
            title=meet.title,
            start_time=meet.start_time,
            author_id=meet.author.id,
            responsible_id=meet.responsible.id,
            participant_statuses=meet.participants,
        )

    def create(self, dto: MeetDTO) -> MeetDTO:
        model = self.model(title=dto.title,
                           category_id=dto.category_id,
                           start_time=dto.start_time,
                           author_id=dto.author_id,
                           responsible_id=dto.responsible_id,
                           )

        model.save()

        # Добавление участников
        # переделать это через метод домена ?
        model.participants.set(dto.participant_statuses.keys())

        # todo тут какая-то херня надо переделать через domain
        # for user_id, status in dto.participant_statuses.items():
        #     user = User.objects.get(id=user_id)
        #     if status == "ABSENT":
        #         status = Status.ABSENT
        #     elif status == "WARNED":
        #         status = Status.WARNED
        #     MeetParticipant.objects.create(
        #         meet=meet, custom_user=user, status=status
        #     )

        return self._orm_to_dto(model)

    def update(self, meet_id: int, dto: MeetDTO) -> MeetDTO:
        repository = IMeetRepository()
        meet = Meet.objects.get(id=meet_id)
        repository.update(meet, dto)
        return self._orm_to_dto(meet)

    def delete(self, meet_id: int) -> None:
        meet = get_object_or_404(Meet, id=meet_id)
        meet.delete()

    def get_meet_by_id(self, meet_id: int):
        return self._orm_to_dto(Meet.objects.get(id=meet_id))

    def get_meets_list(self) -> list[Meet]:
        return [meet for meet in Meet.objects.all()]

    def get_meets_by_category(self, category_id: int) -> list[Meet]:
        return [meet for meet in Meet.objects.filter(category_id=category_id)]


class CategoryRepository(ICategoryRepository, ABC):
    model = Category

    def _orm_to_dto(self, category: Category) -> CategoryObject:
        return CategoryObject(pk=category.id, name=category.name)

    def create(self, category_dto: CategoryObject) -> CategoryObject:
        repository = ICategoryRepository()
        category = CategoryRepository.get_category_by_id(category_dto.id)
        category.name = category_dto.name
        return category

    def update(self, category_id: int, dto: CategoryObject) -> CategoryObject:
        repository = ICategoryRepository()
        category = CategoryRepository.get_category_by_id(category_id)
        category.name = dto.name
        return category

    def delete(self, category_id: int) -> None:
        repository = ICategoryRepository()
        category = CategoryRepository.get_category_by_id(category_id)

    def get_categories_list(self) -> list[CategoryObject]:
        query = self.model.objects.all()
        return [self._orm_to_dto(category) for category in query]

    def get_category_by_id(self, category_id: int) -> CategoryObject:
        query = self.model.objects.get(id=category_id)
        return self._orm_to_dto(query)