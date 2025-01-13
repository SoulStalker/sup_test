from django.conf import settings
from django.core.mail import send_mail
from src.apps.users.repository import UserRepository

from .celery import app

user_repository = UserRepository()


@app.task
def send_email_to_user(**kwargs):
    from_email = settings.DEFAULT_FROM_EMAIL
    name = kwargs.get("name", "")
    email = kwargs.get("email", from_email)
    link = kwargs.get("link", "")
    subject = kwargs.get("subject", f"Добро пожаловать, {name}!")
    message = kwargs.get(
        "message",
        f"Здравствуйте, {name}!\n\nВаш аккаунт успешно создан.\n\nДля подтверждения электронной почты перейдите по ссылке\n\n{link}",
    )
    recipient_list = [email]
    
    send_mail(
        subject, message, from_email, recipient_list, fail_silently=False
    )
