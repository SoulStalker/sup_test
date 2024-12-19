from django.urls import path
from src.apps.verifyemail.views import VerifyEmailUser

app_name = "apps.verifyemail"

urlpatterns = [
    path("<code>/", VerifyEmailUser.as_view(), name="verifyemail"),
]
