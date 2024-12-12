from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.projects.forms import TaskForm
from src.domain.project.dtos import CreateTaskDTO, TaskDTO

User = get_user_model()


class TasksView(BaseView):
    """
    Список проектов
    """

    def get(self, *args, **kwargs):
        tasks = self.task_service.get_tasks_list()
        tasks = self.paginate_queryset(tasks)
        task_status_choices = self.task_service.get_task_status_choices()
        features = self.features_service.get_features_list()
        tags = self.features_service.get_features_tags_list()

        context = {
            "tasks": tasks,
            "users": self.user_service.get_user_list(),
            "task_status_choices": task_status_choices,
            "features": features,
            "tags": tags,
        }
        return render(self.request, "tasks_list.html", context)


class TaskDetailView(BaseView):
    """
    Просмотр проекта
    """

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("task_id")
        task = self.task_service.get_task_by_id(task_id=task_id)
        tags = self.task_service.get_tags_list(task_id=task_id)
        feature = self.features_service.get_feature_by_id(task.feature_id)

        return render(
            request,
            "task_detail.html",
            {
                "task": task,
                "tags": tags,
                "feature": feature,
            },
        )


class CreateTaskView(BaseView):
    """
    Создание проекта
    """

    def get(self, request, *args, **kwargs):
        form = TaskForm(request.POST, request.FILES)

        task_status_choices = self.task_service.get_task_status_choices()

        return render(
            request,
            "create_task_modal.html",
            {
                "form": form,
                "users": self.user_service.get_user_list(),
                "task_status_choices": task_status_choices,
            },
        )

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        # Преобразуем строку с тегами в список
        tags = data.get("tags", "")
        data.setlist("tags", tags.split(","))

        form = TaskForm(data)
        if form.is_valid():
            task_dto = CreateTaskDTO(
                name=form.cleaned_data["name"],
                priority=form.cleaned_data["priority"],
                tags=form.cleaned_data["tags"],
                contributor_id=form.cleaned_data["contributor"].id,
                responsible_id=form.cleaned_data["responsible"].id,
                status=form.cleaned_data["status"],
                closed_at=form.cleaned_data.get("closed_at", None),
                description=form.cleaned_data["description"],
                feature_id=form.cleaned_data["feature"].id,
            )

            try:
                # Создание проекта
                err = self.task_service.create_task(task_dto)
                if err:
                    return JsonResponse(
                        {"status": "error", "message": str(err)}, status=400
                    )
                return JsonResponse({"status": "success"}, status=201)

            except Exception as e:
                print("Error: ", e)
                return JsonResponse(
                    {"status": "error", "message": str(e)}, status=400
                )
        print("Errors: ", form.errors)
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class UpdateTaskView(BaseView):
    """
    Редактирование проекта
    """

    def get(self, request, *args, **kwargs):

        task_id = kwargs.get("task_id")
        task = self.task_service.get_task_by_id(task_id=task_id)

        task_status_choices = self.task_service.get_task_status_choices()

        data = {
            "name": task.name,
            "priority": task.priority,
            "tags": task.tags,
            "contributor": task.contributor_id,
            "responsible": task.responsible_id,
            "status": task.status,
            "created_at": task.created_at,
            "closed_at": task.closed_at,
            "description": task.description,
            "feature": task.feature_id,
            "task_status_choices": task_status_choices,
        }

        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("task_id")
        data = request.POST.copy()
        # Преобразуем строку с тегами в список
        tags = data.get("tags", "")
        data.setlist("tags", tags.split(","))

        form = TaskForm(data)
        if form.is_valid():
            err = self.task_service.update_task(
                TaskDTO(
                    id=task_id,
                    name=form.cleaned_data["name"],
                    priority=form.cleaned_data["priority"],
                    tags=form.cleaned_data["tags"],
                    contributor_id=form.cleaned_data["contributor"].id,
                    responsible_id=form.cleaned_data["responsible"].id,
                    status=form.cleaned_data["status"],
                    created_at=form.cleaned_data.get("created_at", None),
                    closed_at=form.cleaned_data.get("closed_at", None),
                    description=form.cleaned_data["description"],
                    feature_id=form.cleaned_data["feature"].id,
                ),
            )

            if err:
                return JsonResponse(
                    {"status": "error", "message": str(err)}, status=400
                )
            return JsonResponse({"status": "success"}, status=201)
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class DeleteTaskView(BaseView):
    """
    Удаление проекта
    """

    def delete(self, *args, **kwargs):
        task_id = kwargs.get("task_id")
        try:
            self.task_service.delete_task(task_id=task_id)
            return JsonResponse(
                {"status": "success", "message": "Task deleted"}
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=404
            )
