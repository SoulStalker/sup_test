from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from apps.projects.forms import TagForm
from apps.projects.models import Tags


class TagCreateView(generic.CreateView):
    form_class = TagForm
    template_name = "projects/tags.html"
    success_url = reverse_lazy("projects:index")


class TagUpdateView(generic.UpdateView):
    form_class = TagForm
    template_name = "projects/tags_update.html"
    success_url = reverse_lazy("projects:index")

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Tags, slug=slug)
