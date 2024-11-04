from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from apps.projects.forms import featuresForm
from apps.projects.models import features


class featuresCreateView(generic.CreateView):
    form_class = featuresForm
    template_name = "projects/features.html"
    success_url = reverse_lazy("projects:index")


class featuresUpdateView(generic.UpdateView):
    form_class = featuresForm
    template_name = "projects/features_update.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(features, slug=slug)

    def get_success_url(self):
        return reverse_lazy(self.object.get_absolute_url())
