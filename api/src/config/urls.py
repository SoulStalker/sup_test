from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("meets/", include("src.apps.meets.urls", namespace="meets")),
    path("invites/", include("src.apps.invites.urls", namespace="invites")),
    path("projects/", include("src.apps.projects.urls", namespace="projects")),
    path("users/", include("src.apps.users.urls", namespace="users")),
    path("teams/", include("src.apps.teams.urls", namespace="teams")),
    path("registration/", include("src.apps.registration.urls", namespace="registration")),
    path("authorization/", include("src.apps.authorization.urls", namespace="authorization")),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
