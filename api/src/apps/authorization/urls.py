from django.urls import path
from src.apps.authorization.views import Userauthorization

app_name = "apps.authorization"

urlpatterns = [
    path("", Userauthorization.as_view(), name="authorization"),
]
