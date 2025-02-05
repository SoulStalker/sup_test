from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from src.apps.custom_view import BaseView
from src.apps.projects.forms import CommentForm, TaskForm
from src.domain.project import CommentDTO, CreateTaskDTO, TaskDTO

User = get_user_model()


class TasksView(BaseView):
    """
    Список задач
    """

    def get(self, *args, **kwargs):
        tasks = self.task_service.get_list()
        tasks = self.paginate_queryset(tasks)
        task_status_choices = self.task_service.get_task_status_choices()
        features = self.features_service.get_list()
        tags = self.features_service.get_features_tags_list()

        context = {
            "tasks": tasks,
            "users": self.user_service.get_list(),
            "task_status_choices": task_status_choices,
            "features": features,
            "tags": tags,
        }
        return render(self.request, "tasks_list.html", context)


class TaskDetailView(BaseView):
    """
    Просмотр задачи
    """

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("task_id")
        task, error = self.task_service.get_by_id(
            pk=task_id, user_id=self.user_id
        )
        tags = self.task_service.get_tags_list(task_id=task_id)
        comments = self.task_service.get_comments_list(task_id=task_id)
        feature, error = self.features_service.get_by_id(
            task.feature_id, user_id=self.user_id
        )
        print(feature.id, error)
        contributor = self.user_service.get_by_id(
            pk=task.contributor_id, user_id=self.user_id
        )
        responsible = self.user_service.get_by_id(
            pk=task.responsible_id, user_id=self.user_id
        )
        task_url = reverse("projects:tasks")
        return render(
            request,
            "task_detail.html",
            {
                "task": task,
                "tags": tags,
                "feature": feature,
                "contributor": contributor,
                "responsible": responsible,
                "comments": comments,
                "task_url": task_url,
            },
        )

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        task_id = kwargs.get("task_id")
        if form.is_valid():
            comment_dto = CommentDTO(
                user_id=request.user.id,
                task_id=self.task_service.get_by_id(
                    pk=kwargs.get("task_id")
                ).id,
                comment=form.cleaned_data["comment"],
            )
            try:
                self.task_service.create_comment(comment_dto)
                return HttpResponseRedirect(
                    reverse(
                        "projects:task_detail", kwargs={"task_id": task_id}
                    )
                )
            except Exception as e:
                print("Error: ", e)
                return JsonResponse(
                    {"status": "error", "message": str(e)}, status=400
                )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class CreateTaskView(BaseView):
    """
    Создание задачи
    """

    def get(self, request, *args, **kwargs):
        form = TaskForm(request.POST, request.FILES)

        task_status_choices = self.task_service.get_task_status_choices()

        return render(
            request,
            "create_task_modal.html",
            {
                "form": form,
                "users": self.user_service.get_list(),
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
            return self.handle_form(
                form,
                self.task_service.create,
                task_dto,
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class UpdateTaskView(BaseView):
    """
    Редактирование задачи
    """

    def get(self, request, *args, **kwargs):

        task_id = kwargs.get("task_id")
        task, error = self.task_service.get_by_id(
            pk=task_id, user_id=self.user_id
        )
        if error:
            return JsonResponse(
                {"status": "error", "message": error}, status=403
            )
        task_status_choices = self.task_service.get_task_status_choices()

        data = {
            "id": task.id,
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
            task_dto = TaskDTO(
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
            )
            return self.handle_form(
                form,
                self.task_service.update,
                pk=task_id,
                dto=task_dto,
                user_id=self.user_id,
            )
        print(form.errors)
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
            self.task_service.delete(pk=task_id, user_id=self.user_id)
            return JsonResponse(
                {"status": "success", "message": "Task deleted"}
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=404
            )
