from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from apps.projects.forms import FeaturesForm
from apps.projects.models import Features


class FeaturesCreateView(generic.CreateView):
    form_class = FeaturesForm
    template_name = "projects/Featuress.html"
    success_url = reverse_lazy("projects:index")


class FeaturesUpdateView(generic.UpdateView):
    form_class = FeaturesForm
    template_name = "projects/Featuress_update.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Features, slug=slug)

    def get_success_url(self):
        return reverse_lazy(self.object.get_absolute_url())
