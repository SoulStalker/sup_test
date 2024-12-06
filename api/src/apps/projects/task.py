from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.projects.forms import TaskForm
from src.domain.project.dtos import TaskDTO

User = get_user_model()


class TasksView(BaseView):
    """
    Список проектов
    """

    def get(self, *args, **kwargs):
        tasks = self.task_service.get_tasks_list()
        tasks = self.paginate_queryset(tasks)

        context = {
            "tasks": tasks,
            "users": User.objects.order_by("id"),
        }
        return render(self.request, "tasks_list.html", context)


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
                "users": User.objects.order_by("id"),
                "task_status_choices": task_status_choices,
            },
        )

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST, request.FILES)

        if form.is_valid():
            participants = request.POST.getlist("participants")
            task_dto = TaskDTO(
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
                created_task = self.task_service.create_task(task_dto)

                # Возвращаем успешный ответ с данными о созданном проекте
                return JsonResponse(
                    {
                        "status": "success",
                        "task": {
                            "name": created_task.name,
                            "logo": created_task.logo,
                            "slug": created_task.slug,
                            "description": created_task.description,
                            "status": created_task.status,
                            "responsible_id": created_task.responsible_id,
                            "participants": created_task.participants,
                            "date_created": created_task.date_created.isoformat(),
                        },
                    },
                    status=201,
                )

            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)


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
            "logo": task.logo.url if task.logo else None,
            "slug": task.slug,
            "description": task.description,
            "status": task.status,
            "responsible": task.responsible_id,
            "participants": list(task.participants.values("id", "name")),
            "date_created": task.date_created.isoformat(),
            "task_status_choices": task_status_choices,
        }

        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("task_id")
        form = TaskForm(request.POST, request.FILES)

        print(task_id)

        if form.is_valid():
            task = self.task_service.get_task_by_id(task_id=task_id)
            logo = form.cleaned_data.get("logo") if "logo" in request.FILES else None

            print("CD: ", form.cleaned_data)

            self.task_service.update_task(
                task_id=task_id,
                dto=TaskDTO(
                    name=form.cleaned_data["name"],
                    logo=logo if logo else task.logo,
                    description=form.cleaned_data["description"],
                    status=form.cleaned_data["status"],
                    responsible_id=form.cleaned_data["responsible"].id,
                    date_created=form.cleaned_data["date_created"],
                    participants=form.cleaned_data["participants"],
                ),
            )
            try:
                task = self.task_service.get_task_by_id(task_id=task_id)
                return JsonResponse(
                    {
                        "status": "success",
                        "task": {
                            "name": task.name,
                            "logo": task.logo.url if task.logo else None,
                            "slug": task.slug,
                            "description": task.description,
                            "status": task.status,
                            "responsible_id": task.responsible_id,
                            "participants": list(
                                task.participants.values("id", "name")
                            ),
                            "date_created": task.date_created.isoformat(),
                        },
                    },
                    status=201,
                )
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=400)

        print("Errors: ", form.errors)

        return JsonResponse({"status": "error", "errors": form.errors}, status=400)


class DeleteTaskView(BaseView):
    """
    Удаление проекта
    """

    def delete(self, *args, **kwargs):
        task_id = kwargs.get("task_id")
        try:
            self.task_service.delete_task(task_id=task_id)
            return JsonResponse({"status": "success", "message": "Task deleted"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)
