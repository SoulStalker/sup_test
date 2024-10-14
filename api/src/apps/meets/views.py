from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from src.apps.meets.forms import CreateMeetForm
from src.apps.meets.repository import MeetsRepository, CategoryRepository
from src.domain.meet.service import MeetCategoryService, MeetService
from src.domain.meet.dtos import MeetDTO


from django.http import HttpResponseNotAllowed


class MeetsView:
    """
    Список митов
    """
    category_service = MeetCategoryService(CategoryRepository())
    meet_service = MeetService(MeetsRepository(), CategoryRepository())

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    # Метод для маршрутизации запросов
    def dispatch(self):
        allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        if self.request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)

        # Получаем соответствующий метод (например, get, post, delete)
        method = getattr(self, self.request.method.lower(), None)
        return method(self.request, *self.args, **self.kwargs)

    # Создаем метод as_view для интеграции с Django
    @classmethod
    def as_view(cls):
        def meet_view(request, *args, **kwargs):
            self = cls(request, *args, **kwargs)
            return self.dispatch()
        return meet_view

    # @login_required
    def get(self, *args, **kwargs):
        context = {
            "categories": self.category_service.get_categories_list(),
            "users": User.objects.order_by("id"),
            "meets": self.meet_service.get_meets_list(),
        }
        return render(self.request, "meets.html", context)

    # @require_POST
    def delete(self, *args, **kwargs):
        meet_id = kwargs.get("meet_id")
        try:
            self.meet_service.delete(pk=meet_id)
            return JsonResponse({"status": "success", "message": "Meet deleted"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)


class CreateMeetView(LoginRequiredMixin, View):
    """
    Создание мита
    """
    category_service = MeetCategoryService(CategoryRepository())
    meet_service = MeetService(MeetsRepository(), CategoryRepository())

    def get(self, request):
        form = CreateMeetForm(request.POST)
        categories = self.category_service.get_categories_list()
        return render(
            request,
            "create_meet_modal.html",
            {"form": form, "categories": categories},
        )

    def post(self, request):
        form = CreateMeetForm(request.POST)
        if form.is_valid():
            self.meet_service.create(MeetDTO(
                category_id=form.cleaned_data["category"].id,
                title=form.cleaned_data["title"],
                start_time=form.cleaned_data["start_time"],
                author_id=request.user.id,
                responsible_id=form.cleaned_data["responsible"].id,
                participant_statuses=form.cleaned_data["participant_statuses"],
            ))
            return JsonResponse({"status": "success"}, status=201)
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)
