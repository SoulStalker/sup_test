from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.projects.forms import ProjectForm

class ProjectsView(BaseView):
    """
    Список проектов
    """
    items_per_page = 16


    def get(self, *args, **kwargs):
        projects = self.project_service.get_projects_list()

        paginated_projects = self.paginate_queryset(projects)

        for project in projects:
            project.participants.set(project.participants.all())

        context = {
            "projects": paginated_projects['items'],
            "pagination": {
                "current_page": paginated_projects['current_page'],
                "total_pages": paginated_projects['total_pages'],
                "has_next": paginated_projects['has_next'],
                "has_previous": paginated_projects['has_previous'],
                "page_range": paginated_projects['page_range'],
            },
        }

        return render(self.request, "projects.html", context)

class CreateProjectView(BaseView):
    """
    Создание проекта
    """
    def get(self, request, *args, **kwargs):
        form = ProjectForm(request.POST or None)

        return render(
            request,
            "create_project_modal.html",
            {"form": form},
        )