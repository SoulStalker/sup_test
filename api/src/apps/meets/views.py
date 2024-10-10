from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

# from apps.meets.choice_classes import StatusChoice
from src.apps.meets.forms import CreateMeetForm
from src.apps.meets.repository import MeetsRepository, CategoryRepository
from src.domain.meet.service import MeetCategoryService, MeetService
from src.domain.meet.dtos import MeetDTO, CategoryDTO
from src.models.meets import Meet


# from apps.meets.models import Category, Meet, MeetParticipant, User


class MeetsView(LoginRequiredMixin, TemplateView):
    template_name = "meets.html"

    def __init__(self):
        super().__init__()
        self.category_service = MeetCategoryService(CategoryRepository)
        self.meet_service = MeetService(MeetsRepository, CategoryRepository)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = MeetCategoryService.get_list
        context["users"] = User.objects.order_by("id")
        # context["meets"] = Meet.objects.prefetch_related("participants").all()
        context["meets"] = self.meet_service.get_meets_list()

        return context


@require_POST
def delete_meet(request, meet_id):
    try:
        meet = get_object_or_404(Meet, id=meet_id)
        meet.delete()
        return JsonResponse({"status": "success"})
    except Meet.DoesNotExist:
        return JsonResponse({"status": "Meet not found"}, status=404)


class CreateMeetView(LoginRequiredMixin, View):
    """
    Создание мита
    """
    def __init__(self):
        super().__init__()
        self.category_service = MeetCategoryService(CategoryRepository())
        self.meet_service = MeetService(MeetsRepository())
    # def get(self, request):
    #     form = CreateMeetForm(request.POST)
    #     categories = MeetCategoryService.get_list
    #     return render(
    #         request,
    #         "create_meet_modal.html",
    #         {"form": form, "categories": categories},
    #     )

    def post(self, request):
        form = CreateMeetForm(request.POST)
        if form.is_valid():
            # data = form.cleaned_data
            self.meet_service.create(MeetDTO(
                category=form.cleaned_data["category"],
                title=form.cleaned_data["title"],
                start_time=form.cleaned_data["start_time"],
                author_id=form.cleaned_data["author_id"],
                responsible_id=form.cleaned_data["responsible_id"],
                participants_ids=form.cleaned_data["participants_ids"],
            ))


            # participant_statuses = data["participant_statuses"]
            # for user_id, status in participant_statuses.items():
            #     user = User.objects.get(id=user_id)
            #     if status == "ABSENT":
            #         status = StatusChoice.ABSENT
            #     elif status == "WARNED":
            #         status = StatusChoice.WARNED
            #     MeetParticipant.objects.create(
            #         meet=meet, custom_user=user, status=status
            #     )

            return JsonResponse({"status": "success"}, status=201)

        return render(request, "create_meet_modal.html", {"form": form})
