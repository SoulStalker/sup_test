# from django.urls import reverse_lazy
# from django.views import generic

# from apps.projects.forms import TaskForm


# class TaskCreateView(generic.CreateView):
#     form_class = TaskForm
#     template_name = "projects/tasks_create.html"
#     success_url = reverse_lazy("projects:index")

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# class TaskUpdateView(generic.UpdateView):
#     form_class = TaskForm
#     template_name = "projects/tasks_update.html"
#     success_url = reverse_lazy("projects:index")
#     slug_url_kwarg = "slug"
