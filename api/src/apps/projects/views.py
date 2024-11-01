from pprint import pprint

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse

from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.projects.forms import ProjectForm
from src.models.choice_classes import ProjectChoices
from src.domain.project.dtos import ProjectDTO



class ProjectsView(BaseView):
    """
    Список проектов
    """
    items_per_page = 16


    def get(self, *args, **kwargs):
        projects = self.project_service.get_projects_list()

        paginated_projects = self.paginate_queryset(projects)

        project_status_choices = self.project_service.get_project_status_choices()

        for project in projects:
            project.participants.set(project.participants.all())

        context = {
            "projects": paginated_projects['items'],
            "users": User.objects.order_by("id"),
            "project_status_choices": project_status_choices,
            "pagination": {
                "current_page": paginated_projects['current_page'],
                "total_pages": paginated_projects['total_pages'],
                "has_next": paginated_projects['has_next'],
                "has_previous": paginated_projects['has_previous'],
                "page_range": paginated_projects['page_range'],
            },
        }

        pprint(paginated_projects)

        return render(self.request, "projects.html", context)

class CreateProjectView(BaseView):
    """
    Создание проекта
    """
    def get(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)

        project_status_choices = self.project_service.get_project_status_choices()

        return render(
            request,
            "create_project_modal.html",
            {
                "form": form,
                "users": User.objects.order_by("id"),
                "project_status_choices": project_status_choices
             },
        )

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)

        if form.is_valid():
            participants = request.POST.getlist('participants')
            project_dto = ProjectDTO(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                status=form.cleaned_data["status"],
                participants=participants,
                responsible_id=form.cleaned_data["responsible"].id,
                date_created=form.cleaned_data["date_created"],
            )

            try:
                # Создание проекта
                created_project = self.project_service.create_project(project_dto)

                # Возвращаем успешный ответ с данными о созданном проекте
                return JsonResponse({
                    "status": "success",
                    "project": {
                        "name": created_project.name,
                        "slug": created_project.slug,
                        "description": created_project.description,
                        "status": created_project.status,
                        "responsible_id": created_project.responsible_id,
                        "participants": created_project.participants,
                        "date_created": created_project.date_created.isoformat(),
                    }
                }, status=201)

            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)

class EditProjectView(BaseView):
    """
    Редактирование проекта
    """
    def get(self, request, *args, **kwargs):
        project_id = kwargs.get("project_id")
        project = self.project_service.get_project(pk=project_id)

        project_status_choices = self.project_service.get_project_status_choices()

        data = {
            "name": project.name,
            "slug": project.slug,
            "description": project.description,
            "status": project.status,
            "responsible": project.responsible_id,
            "participants": project.participants,
            "date_created": project.date_created.isoformat(),
            "project_status_choices": project_status_choices
        }

        return JsonResponse(data)