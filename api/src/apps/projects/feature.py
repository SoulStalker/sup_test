# from django.shortcuts import get_object_or_404
# from django.urls import reverse_lazy
# from django.views import generic

# from apps.projects.forms import FeatureForm
# from apps.projects.models import Feature


# class FeatureCreateView(generic.CreateView):
#     form_class = FeatureForm
#     template_name = "projects/features.html"
#     success_url = reverse_lazy("projects:index")


# class FeatureUpdateView(generic.UpdateView):
#     form_class = FeatureForm
#     template_name = "projects/features_update.html"

#     def get_object(self, queryset=None):
#         slug = self.kwargs.get("slug")
#         return get_object_or_404(Feature, slug=slug)

#     def get_success_url(self):
#         return reverse_lazy(self.object.get_absolute_url())
