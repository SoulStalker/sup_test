from django.urls import path
from src.apps.registration.views import UserRegistration



app_name = "apps.registration"


urlpatterns = [
    path("<invitation_code>/", UserRegistration.as_view(), name="registration"),
]
