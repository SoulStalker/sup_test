from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import TemplateView

from src.apps.meets.forms import CreateMeetForm
from src.apps.meets.repository import MeetsRepository, CategoryRepository
from src.domain.meet.service import MeetCategoryService, MeetService
from src.domain.meet.dtos import MeetDTO


from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


class MeetsView:
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.category_service = MeetCategoryService(CategoryRepository())
        self.meet_service = MeetService(MeetsRepository(), CategoryRepository())

    # Метод для маршрутизации запросов
    def dispatch(self):
        allowed_methods = ["GET", "PUT", "PATCH", "DELETE", "POST"]

        if self.request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)

        method = getattr(self, self.request.method.lower())
        return method()

    # Создаем метод as_view для интеграции с Django
    @classmethod
    def as_view(cls):
        def meet_view(request, *args, **kwargs):
            return MeetsView(request).dispatch()
            # self = cls(request, *args, **kwargs)
            # return self.dispatch()
        return meet_view

    # Обработка GET запросов
    # @method_decorator(login_required)
    def get(self):
        context = {
            "categories": self.category_service.get_categories_list(),
            "users": User.objects.order_by("id"),
            "meets": self.meet_service.get_meets_list(),
        }
        return render(self.request, "meets.html", context)

    def delete(self, *args, **kwargs):

        print(f"kwargs: {kwargs}")

        meet_id = kwargs.get("meet_id")
        print(meet_id)
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
    # def __init__(self):
    #     super().__init__()
    #     self.category_service = MeetCategoryService(CategoryRepository())
    #     self.meet_service = MeetService(MeetsRepository(), CategoryRepository())

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

        print("Ошибка при создании мита из формы: ", form.errors.get_json_data())

        return JsonResponse({"status": "error", "errors": form.errors}, status=400)
