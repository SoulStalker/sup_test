from django.urls import reverse_lazy
from django.views import generic

from apps.projects.forms import ProjectForm


class ProjectCreateView(generic.CreateView):
    form_class = ProjectForm
    template_name = "projects/projects_create.html"
    success_url = reverse_lazy("projects:index")

    def form_valid(self, form):
        form.instance.responsible = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(generic.UpdateView):
    form_class = ProjectForm
    template_name = "projects/projects_update.html"
    success_url = reverse_lazy("projects:index")
