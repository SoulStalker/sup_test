from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from src.apps.meets.forms import CreateMeetForm
from src.apps.meets.repository import MeetsRepository, CategoryRepository
from src.domain.meet.service import MeetCategoryService, MeetService
from src.domain.meet.dtos import MeetDTO


class MeetsView(LoginRequiredMixin, TemplateView):
    template_name = "meets.html"

    category_service = MeetCategoryService(CategoryRepository())
    meet_service = MeetService(MeetsRepository(), CategoryRepository())

    # def __init__(self):
    #     super().__init__()
    #     self.category_service = MeetCategoryService(CategoryRepository())
    #     self.meet_service = MeetService(MeetsRepository(), CategoryRepository())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.category_service.get_categories_list()
        context["users"] = User.objects.order_by("id")
        context["meets"] = self.meet_service.get_meets_list()
        return context

    @staticmethod
    @require_POST
    def delete_meet(request, meet_id):
        try:
            MeetService(MeetsRepository(), CategoryRepository()).delete(pk=meet_id)
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": e}, status=404)


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
