from pprint import pprint

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from src.apps.custom_view import BaseView
from src.apps.meets.forms import CreateMeetForm
from src.domain.meet.dtos import MeetDTO


class MeetsView(BaseView):
    """
    Список митов
    """
    items_per_page = 16

    def get(self, *args, **kwargs):

        meets = self.meet_service.get_meets_list()
        paginated_meets = self.paginate_queryset(meets)

        context = {
            "categories": self.category_service.get_categories_list(),
            "users": User.objects.order_by("id"),
            "meets": paginated_meets['items'],
            "pagination": {
                "current_page": paginated_meets['current_page'],
                "total_pages": paginated_meets['total_pages'],
                "has_next": paginated_meets['has_next'],
                "has_previous": paginated_meets['has_previous'],
                "page_range": paginated_meets['page_range'],
            }
        }

        pprint(paginated_meets)

        return render(self.request, "meets.html", context)

    def delete(self, *args, **kwargs):
        meet_id = kwargs.get("meet_id")
        try:
            self.meet_service.delete(pk=meet_id)
            return JsonResponse({"status": "success", "message": "Meet deleted"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)


class CreateMeetView(BaseView):
    """
    Создание мита
    """

    def get(self, request, *args, **kwargs):
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
            err = self.meet_service.create(MeetDTO(
                category_id=form.cleaned_data["category"].id,
                title=form.cleaned_data["title"],
                start_time=form.cleaned_data["start_time"],
                author_id=request.user.id,
                responsible_id=form.cleaned_data["responsible"].id,
                participant_statuses=form.cleaned_data["participant_statuses"],
            ))
            if err:
                return JsonResponse({"status": "error", "message": str(err)}, status=400)
            return JsonResponse({"status": "success"}, status=201)
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)


class EditMeetView(BaseView):
    """
    Получение данных для редактирования мита
    """
    def get(self, request, *args, **kwargs):
        meet_id = kwargs.get("meet_id")
        statuses = self.meet_service.get_participants_statuses(meet_id)
        meet = self.meet_service.get_meet(meet_id)

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
            self.meet_service.update(meet_id=meet_id, dto=MeetDTO(
                category_id=form.cleaned_data["category"].id,
                title=form.cleaned_data["title"],
                start_time=form.cleaned_data["start_time"],
                author_id=request.user.id,
                responsible_id=form.cleaned_data["responsible"].id,
                participant_statuses=form.cleaned_data["participant_statuses"],
            ))
            return JsonResponse({"status": "success"}, status=201)

        return JsonResponse({"status": "error", "errors": form.errors}, status=400)


class CategoryView(BaseView):
    def get(self, request, *args, **kwargs):
        categories = self.category_service.get_categories_list()
        return JsonResponse({"categories": categories})

    def post(self, request, *args, **kwargs):
        category_name = request.POST.get('category_name')
        if category_name:
            # Создаем новую категорию
            # category = Category.objects.create(name=category_name)
            category = self.category_service.create(category_name)
            print(category)
            return JsonResponse({"status": "success", "category_id": category.pk, "category_name": category.name})
        else:
            return JsonResponse({"status": "error", "error": "Название категории не может быть пустым."})
