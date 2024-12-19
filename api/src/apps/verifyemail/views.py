from src.apps.custom_view import BaseView
from django.shortcuts import render


class VerifyEmailUser(BaseView):
    """Регистрация пользователя"""

    def get(self, request, code):
        self.verifyemail_service.chek_verify_code_or_404(code)
        return render(
            request,
            "welkome.html",
        )
