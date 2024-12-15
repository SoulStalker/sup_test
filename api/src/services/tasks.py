from django.conf import settings
from django.core.mail import send_mail
from src.apps.users.repository import UserRepository

from .celery import app

user_repository = UserRepository()


@app.task
def send_email_to_user(**kwargs):
    subject = kwargs.get("subject", f"Добро пожаловать, {kwargs.get('name')}!")
    message = kwargs.get(
        "message",
        f"Здравствуйте, {kwargs.get("name")}!\n\nВаш аккаунт успешно создан.",
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [kwargs.get("email")]
    send_mail(
        subject, message, from_email, recipient_list, fail_silently=False
    )
