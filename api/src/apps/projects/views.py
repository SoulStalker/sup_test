from pprint import pprint

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse

from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.projects.forms import ProjectForm, CreateFeaturesForm
from src.models.choice_classes import ProjectChoices, FeaturesChoices
from src.domain.project.dtos import ProjectDTO, FeaturesDTO



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
        form = ProjectForm(request.POST, request.FILES)

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
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            participants = request.POST.getlist('participants')
            project_dto = ProjectDTO(
                name=form.cleaned_data["name"],
                logo=form.cleaned_data["logo"],
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
                        "logo": created_project.logo,
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
        project = self.project_service.get_project_by_id(project_id=project_id)

        project_status_choices = self.project_service.get_project_status_choices()

        data = {
            "name": project.name,
            "logo": project.logo.url if project.logo else None,
            "slug": project.slug,
            "description": project.description,
            "status": project.status,
            "responsible": project.responsible_id,
            "participants": list(project.participants.values("id", "username")),
            "date_created": project.date_created.isoformat(),
            "project_status_choices": project_status_choices
        }

        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        project_id = kwargs.get("project_id")
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = self.project_service.get_project_by_id(project_id=project_id)
            logo = form.cleaned_data.get("logo") if "logo" in request.FILES else None
            self.project_service.update_project(project_id=project_id, dto=ProjectDTO(
                name=form.cleaned_data["name"],
                logo=logo if logo else project.logo,
                description=form.cleaned_data["description"],
                status=form.cleaned_data["status"],
                responsible_id=form.cleaned_data["responsible"].id,
                date_created=form.cleaned_data["date_created"],
                participants=form.cleaned_data["participants"],
            ))
            try:
                project = self.project_service.get_project_by_id(project_id=project_id)
                return JsonResponse({
                    "status": "success",
                    "project": {
                        "name": project.name,
                        "logo": project.logo.url if project.logo else None,
                        "slug": project.slug,
                        "description": project.description,
                        "status": project.status,
                        "responsible_id": project.responsible_id,
                        "participants": list(project.participants.values("id", "username")),
                        "date_created": project.date_created.isoformat(),
                    }
                }, status=201)
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)

        return JsonResponse({"status": "error", "errors": form.errors}, status=400)


class DeleteProjectView(BaseView):
    """
    Удаление проекта
    """
    def delete(self, *args, **kwargs):
        project_id = kwargs.get("project_id")
        try:
            self.project_service.delete_project(project_id=project_id)
            return JsonResponse({"status": "success", "message": "Project deleted"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)


class SearchProjectView(BaseView):
    """
    Поиск проектов
    """
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        projects = self.project_service.search_projects(query=query)

        if not projects:
            return render(self.request, "projects.html", {"projects": [], "query": query})
        return render(self.request, "projects.html", {"projects": projects, "query": query})



class FeaturesView(BaseView):

    items_per_page = 16

    def get(self, request, *args, **kwargs):
        features = self.features_service.get_features_list()
        tags = self.features_service.get_features_tags_list()
        statuses = self.features_service.get_features_status_list()
        projectes = self.features_service.get_feature_project_list()


        return render(request, "features.html", {
            "features": features,
            "users": User.objects.order_by("id"),
            "tags": tags,
            "statuses": [str(status) for status in statuses],
            "project": projectes
        })

class CreateFeatureView(BaseView):
    def get(self, request, *args, **kwargs):
        form = CreateFeaturesForm(request.POST)
        tags = self.features_service.get_features_tags_list()
        statuses = self.features_service.get_features_status_list()
        projectes = self.features_service.get_feature_project_list()


        return render(
            request,
            "create_features_modal.html",
            {
                "form": form,
                "users": User.objects.order_by("id"),
                "tags": tags,
                "statuses": [str(status) for status in statuses],
                "project": projectes
             },
        )

    def post(self, request, *args, **kwargs):
        form = CreateFeaturesForm(request.POST)
        if form.is_valid():
            tags = request.POST.getlist('tags')
            participants = request.POST.getlist('participants')
            features_dto = (FeaturesDTO(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                status=form.cleaned_data["status"],
                responsible_id=form.cleaned_data["responsible"].id,
                participants=list(participants),
                importance=form.cleaned_data["importance"],
                tags=list(tags),  # Передаем список ID тегов
                project_id=form.cleaned_data["project"].id
            ))
            try:
                created_feature = self.features_service.create_features(features_dto)

                # Возвращаем успешный ответ с данными о созданной функции
                return JsonResponse({
                    "status": "success",
                    "feature": {
                        "name": created_feature.name,
                        "description": created_feature.description,
                        "status": created_feature.status,
                        "responsible_id": created_feature.responsible_id,
                        "importance": created_feature.importance,
                        "participants": list(participants),
                        "tags": list(tags),
                        "project_id": created_feature.project_id,
                    }
                }, status=201)

            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)

        return JsonResponse({"status": "error", "errors": form.errors}, status=400)


class EditFeatureView(BaseView):
    def get(self, request, *args, **kwargs):
        feature_id = kwargs.get("feature_id")
        feature = self.features_service.get_feature_by_id(feature_id=feature_id)

        data = {
            "name": feature.name,
            "description": feature.description,
            "status": feature.status,
            "responsible": feature.responsible_id,
            "importance": feature.importance,
            "tags": feature.tags,
            "participants": feature.participants,
            "project": feature.project_id,
        }

        return JsonResponse(data)


    def post(self, request, *args, **kwargs):
        feature_id = kwargs.get("feature_id")
        form = CreateFeaturesForm(request.POST)

        if form.is_valid():
            # Получаем данные из формы
            tags = request.POST.getlist('tags')
            participants = request.POST.getlist('participants')

            # Создаем объект DTO для фичи
            features_dto = FeaturesDTO(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                status=form.cleaned_data["status"],
                responsible_id=form.cleaned_data["responsible"].id,
                participants=list(participants),  # Убедитесь, что передаете ID участников
                importance=form.cleaned_data["importance"],
                tags=list(tags),  # Убедитесь, что передаете ID тегов
                project_id=form.cleaned_data["project"].id,
            )

            try:
                updated_feature = self.features_service.update_features(feature_id=feature_id, dto=features_dto)
                return JsonResponse({
                    "status": "success",
                    "feature": {
                        "name": updated_feature.name,
                        "description": updated_feature.description,
                        "status": updated_feature.status,
                        "responsible_id": updated_feature.responsible_id,
                        "importance": updated_feature.importance,
                        "participants": updated_feature.participants,
                        "tags": updated_feature.tags,
                        "project_id": updated_feature.project_id,
                    }
                }, status=200)  # Статус 200 для успешного обновления

            except Exception as e:
                print(f"Ошибка при обновлении фичи: {e}")
                return JsonResponse({"status": "error", "message": str(e)}, status=400)

        else:
            print(f"Ошибки формы: {form.errors}")
            return JsonResponse({
                "status": "error",
                "errors": form.errors
            }, status=400)

