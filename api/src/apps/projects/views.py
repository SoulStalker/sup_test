from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from src.apps.custom_view import BaseView
from src.apps.projects.forms import CreateFeaturesForm, ProjectForm
from src.domain.project import CreateFeaturesDTO, ProjectDTO

User = get_user_model()


class ProjectsView(BaseView):
    """
    Список проектов
    """

    items_per_page = 16

    def get(self, *args, **kwargs):
        projects = self.project_service.get_list()

        project_status_choices = (
            self.project_service.get_project_status_choices()
        )

        for project in projects:
            project.participants.set(project.participants.all())
        projects = self.paginate_queryset(projects)
        features_url = reverse("projects:features")
        users = self.user_service.get_active_users()

        context = {
            "projects": projects,
            "users": users,
            # тут косяк. идет прямой запрос в базу
            "project_status_choices": project_status_choices,
            "features_url": features_url,
        }
        return render(self.request, "projects_list.html", context)


class CreateProjectView(BaseView):
    """
    Создание проекта
    """

    def get(self, request, *args, **kwargs):
        form = ProjectForm(request.POST, request.FILES)
        project_status_choices = (
            self.project_service.get_project_status_choices()
        )
        return render(
            request,
            "create_project_modal.html",
            {
                "form": form,
                "users": User.objects.order_by("id"),
                "project_status_choices": project_status_choices,
            },
        )

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            participants = request.POST.getlist("participants")
            return self.handle_form(
                form,
                self.project_service.create,
                ProjectDTO(
                    name=form.cleaned_data["name"],
                    logo=form.cleaned_data["logo"],
                    description=form.cleaned_data["description"],
                    status=form.cleaned_data["status"],
                    participants=participants,
                    responsible_id=form.cleaned_data["responsible"].id,
                    date_created=form.cleaned_data["date_created"],
                ),
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class EditProjectView(BaseView):
    """
    Редактирование проекта
    """
    def get(self, request, *args, **kwargs):
        project_id = kwargs.get("project_id")
        if not project_id:
            return JsonResponse(
                {"status": "error", "message": "ID проекта не указан"}, status=400
            )
        project, error = self.project_service.get_by_id(
            pk=project_id, user_id=self.user_id
        )
        if error:
            return JsonResponse(
                {"status": "error", "message": error}, status=403
            )
        # Проверяем, существует ли проект
        if not project:
            return JsonResponse(
                {"status": "error", "message": "Проект не найден"}, status=404
            )
        project_status_choices = (
            self.project_service.get_project_status_choices()
        )
        data = {
            "name": project.name,
            "logo": project.logo.url if project.logo else None,
            "slug": project.slug,
            "description": project.description,
            "status": project.status,
            "responsible": project.responsible_id,
            "participants": list(project.participants.values("id", "name")),
            "date_created": project.date_created.isoformat(),
            "project_status_choices": project_status_choices,
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        project_id = kwargs.get("project_id")
        if not project_id:
            return JsonResponse(
                {"status": "error", "message": "ID проекта не указан"}, status=400
            )
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project, error = self.project_service.get_by_id(
                pk=project_id, user_id=self.user_id
            )
            if error:
                return JsonResponse(
                    {"status": "error", "message": error}, status=403
                )
            # Проверяем, существует ли проект
            if not project:
                return JsonResponse(
                    {"status": "error", "message": "Проект не найден"}, status=404
                )

            # Обработка логотипа
            logo = None
            if "logo" in request.FILES:
                logo_file = request.FILES["logo"]
                if logo_file.size > MAX_FILE_SIZE:  # Например, 5 MB
                    return JsonResponse(
                        {"status": "error", "errors": {"logo": ["Файл слишком большой"]}},
                        status=400
                    )
                logo = logo_file

            # Создаем DTO
            project_dto = ProjectDTO(
                name=form.cleaned_data["name"],
                logo=logo if logo else project.logo,
                description=form.cleaned_data["description"],
                status=form.cleaned_data["status"],
                responsible_id=form.cleaned_data["responsible"].id,
                date_created=form.cleaned_data["date_created"],
                participants=form.cleaned_data["participants"],
            )

            # Обработка формы через handle_form
            return self.handle_form(
                form,
                self.project_service.update,
                project_id,
                project_dto,
                self.user_id,
            )
        else:
            # Возвращаем ошибки формы в формате JSON
            errors = {field: error_list for field, error_list in form.errors.items()}
            return JsonResponse({"status": "error", "errors": errors}, status=400)

    def handle_form(self, form, service_method, *args, **kwargs):
        try:
            result = service_method(*args, **kwargs)
            return JsonResponse({"status": "success", "message": "Операция выполнена успешно"})
        except Exception as e:
            # Логируем ошибку
            print(traceback.format_exc())
            return JsonResponse(
                {"status": "error", "message": f"Произошла ошибка: {str(e)}"},
                status=500
            )

class DeleteProjectView(BaseView):
    """
    Удаление проекта
    """

    def delete(self, *args, **kwargs):
        project_id = kwargs.get("project_id")
        try:
            error = self.project_service.delete(
                pk=project_id, user_id=self.user_id
            )
            if error:
                return JsonResponse(
                    {"status": "error", "message": error}, status=403
                )
            return JsonResponse(
                {"status": "success", "message": "Meet deleted"}
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=403
            )


class SearchProjectView(BaseView):
    """
    Поиск проектов
    """

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        projects = self.project_service.search_projects(query=query)

        if not projects:
            return render(
                self.request, "projects.html", {"projects": [], "query": query}
            )
        return render(
            self.request,
            "projects.html",
            {"projects": projects, "query": query},
        )


class FeaturesView(BaseView):
    """Список фичей"""

    items_per_page = 16

    def get(self, request, *args, **kwargs):
        features = self.features_service.get_list()
        tags = self.features_service.get_features_tags_list()
        statuses = self.features_service.get_features_status_list()
        projects = self.features_service.get_feature_project_list()
        task_url = reverse("projects:tasks")
        users = self.user_service.get_active_users()

        return render(
            request,
            "features.html",
            {
                "features": features,
                "users": users,
                "tags": tags,
                "statuses": [str(status) for status in statuses],
                "project": projects,
                "task_url": task_url,
            },
        )


class FeaturesDetailView(BaseView):
    """Просмотр фичи"""

    def get(self, request, *args, **kwargs):
        feature_id = kwargs.get("features_id")
        feature, error = self.features_service.get_by_id(
            pk=feature_id, user_id=self.user_id
        )
        project, error = self.project_service.get_by_id(
            pk=feature.project_id, user_id=self.user_id
        )
        users = self.user_service.get_user_id_list(
            user_list_id=feature.participants
        )
        tags = self.task_service.get_tags_id_list(tags_id=feature.tags)
        tasks = self.task_service.get_task_id_list(dto=feature)
        return render(
            request,
            "features_detail.html",
            {
                "feature": feature,
                "users": users,
                "project": project,
                "tags": tags,
                "tasks": tasks,
            },
        )


class CreateFeatureView(BaseView):
    def get(self, request, *args, **kwargs):
        form = CreateFeaturesForm(request.POST)
        tags = self.features_service.get_features_tags_list()
        statuses = self.features_service.get_features_status_list()
        projects = self.features_service.get_feature_project_list()

        return render(
            request,
            "create_features_modal.html",
            {
                "form": form,
                "users": User.objects.order_by("id"),
                "tags": tags,
                "statuses": [str(status) for status in statuses],
                "project": projects,
            },
        )

    def post(self, request, *args, **kwargs):
        form = CreateFeaturesForm(request.POST)
        if form.is_valid():
            tags = request.POST.getlist("tags")
            participants = request.POST.getlist("participants")
            features_dto = CreateFeaturesDTO(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                status=form.cleaned_data["status"],
                responsible_id=form.cleaned_data["responsible"].id,
                participants=list(participants),
                importance=form.cleaned_data["importance"],
                tags=list(tags),  # Передаем список ID тегов
                project_id=form.cleaned_data["project"].id,
            )
            return self.handle_form(
                form,
                self.features_service.create,
                features_dto,
                self.user_id,
            )

        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class EditFeatureView(BaseView):
    def get(self, request, *args, **kwargs):
        feature_id = kwargs.get("feature_id")
        feature, error = self.features_service.get_by_id(
            pk=feature_id, user_id=self.user_id
        )
        if error:
            return JsonResponse(
                {"status": "error", "message": error}, status=403
            )
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
            tags = request.POST.getlist("tags")
            participants = request.POST.getlist("participants")

            # Создаем объект DTO для фичи
            features_dto = CreateFeaturesDTO(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                status=form.cleaned_data["status"],
                responsible_id=form.cleaned_data["responsible"].id,
                participants=list(
                    participants
                ),  # Убедитесь, что передаете ID участников
                importance=form.cleaned_data["importance"],
                tags=list(tags),  # Убедитесь, что передаете ID тегов
                project_id=form.cleaned_data["project"].id,
            )

            print(features_dto)

            return self.handle_form(
                form,
                self.features_service.update,
                feature_id,
                features_dto,
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class DeleteFeatureView(BaseView):
    def delete(self, *args, **kwargs):
        feature_id = kwargs.get("feature_id")
        try:
            self.features_service.delete(pk=feature_id, user_id=self.user_id)
            return JsonResponse(
                {"status": "success", "message": "Feature deleted"}
            )
        except Exception as e:
            print("Error: ", e)
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=403
            )


class SearchFeatureView(BaseView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        features = self.features_service.get_search_features(query=query)

        if not features:
            return render(
                self.request, "features.html", {"features": [], "query": query}
            )
        return render(
            self.request,
            "features.html",
            {"features": features, "query": query},
        )
