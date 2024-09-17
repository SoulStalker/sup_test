from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from apps.meets.choice_classes import StatusChoice
from apps.meets.forms import CreateMeetForm
from apps.meets.models import Category, Meet, MeetParticipant, User


class MeetsView(LoginRequiredMixin, TemplateView):
    template_name = "meets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["users"] = User.objects.order_by("id")
        context["meets"] = Meet.objects.prefetch_related("participants").all()

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

    def get(self, request):
        form = CreateMeetForm()
        categories = Category.objects.all()
        return render(
            request,
            "create_meet_modal.html",
            {"form": form, "categories": categories},
        )

    def post(self, request):
        form = CreateMeetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            meet = Meet.objects.create(
                author=request.user,
                title=data["title"],
                start_date=data["start_date"],
                start_time=data["start_time"],
                category=data["category"],
                responsible=data["responsible"],
            )

            meet.save()

            participant_statuses = data["participant_statuses"]
            for user_id, status in participant_statuses.items():
                user = User.objects.get(id=user_id)
                if status == "ABSENT":
                    status = StatusChoice.ABSENT
                elif status == "WARNED":
                    status = StatusChoice.WARNED
                MeetParticipant.objects.create(
                    meet=meet, custom_user=user, status=status
                )

            return JsonResponse({"status": "success"}, status=201)

        return render(request, "create_meet_modal.html", {"form": form})
