from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.meets.forms import CreateMeetForm
from src.domain.meet import MeetDTO, MeetEntity

User = get_user_model()


class MeetsView(BaseView):
    """
    Список митов
    """

    def get(self, *args, **kwargs):
        user_id = self.request.user.id
        categories = self.category_service.get_list(user_id)
        users = self.user_service.get_list(user_id)
        meets = self.meet_service.get_list(user_id)
        meets = self.paginate_queryset(meets)

        return render(
            self.request,
            "meets_list.html",
            {
                "categories": categories,
                "users": users,
                "meets": meets,
            },
        )

    def delete(self, *args, **kwargs):
        meet_id = kwargs.get("meet_id")
        user_id = self.request.user.id
        try:
            error = self.meet_service.delete(pk=meet_id, user_id=user_id)
            if error:
                return JsonResponse(
                    {"status": "error", "message": error}, status=403
                )
            return JsonResponse(
                {"status": "success", "message": "Meet deleted"}
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=404
            )


class CreateMeetView(BaseView):
    """
    Создание мита
    """

    def get(self, request, *args, **kwargs):
        form = CreateMeetForm(request.POST)
        categories = self.category_service.get_list()
        return render(
            request,
            "create_meet_modal.html",
            {"form": form, "categories": categories},
        )

    def post(self, request):
        form = CreateMeetForm(request.POST)
        if form.is_valid():
            return self.handle_form(
                form,
                self.meet_service.create,
                MeetEntity(
                    category_id=form.cleaned_data["category"].id,
                    title=form.cleaned_data["title"],
                    start_time=form.cleaned_data["start_time"],
                    author_id=request.user.id,
                    responsible_id=form.cleaned_data["responsible"].id,
                    participant_statuses=form.cleaned_data[
                        "participant_statuses"
                    ],
                ),
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class EditMeetView(BaseView):
    """
    Получение данных для редактирования мита
    """

    def get(self, request, *args, **kwargs):
        meet_id = kwargs.get("meet_id")
        statuses = self.meet_service.get_participants_statuses(meet_id)
        meet, error = self.meet_service.get_by_id(meet_id, self.user_id)
        if error:
            return JsonResponse(
                {"status": "error", "message": error}, status=403
            )
        data = {
            "title": meet.title,
            "start_time": meet.start_time.strftime("%Y-%m-%dT%H:%M"),
            "category": meet.category_id,
            "responsible": meet.responsible_id,
            "participants": [vars(item) for item in statuses],
        }

        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        meet_id = kwargs.get("meet_id")
        form = CreateMeetForm(request.POST)
        if form.is_valid():
            return self.handle_form(
                form,
                self.meet_service.update,
                meet_id,
                MeetDTO(
                    id=meet_id,
                    category_id=form.cleaned_data["category"].id,
                    title=form.cleaned_data["title"],
                    start_time=form.cleaned_data["start_time"],
                    author_id=request.user.id,
                    responsible_id=form.cleaned_data["responsible"].id,
                    participant_statuses=form.cleaned_data[
                        "participant_statuses"
                    ],
                ),
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class CategoryView(BaseView):
    def get(self, request, *args, **kwargs):
        categories = self.category_service.get_list()
        return JsonResponse({"categories": categories})

    def post(self, request, *args, **kwargs):
        try:
            category_name = request.POST.get("category_name")
            if category_name:
                # Создаем новую категорию
                category, err = self.category_service.create(category_name)
                if err:
                    return JsonResponse(
                        {"status": "error", "error": str(err)}, status=400
                    )
                return JsonResponse(
                    {
                        "status": "success",
                        "category_id": category.pk,
                        "category_name": category.name,
                    }
                )
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "error": "Название категории не может быть пустым.",
                    }
                )
        except IntegrityError:
            return JsonResponse(
                {"status": "error", "error": "Такая категория уже существует"},
                status=400,
            )
        except Exception as err:
            return JsonResponse(
                {"status": "error", "error": str(err)}, status=400
            )
