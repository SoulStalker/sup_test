from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("meets/", include("src.apps.meets.urls", namespace="meets")),
    path("users/", include("src.apps.users.urls", namespace="users")),
]
