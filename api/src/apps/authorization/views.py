from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from src.apps.authorization.forms import AuthorizationForm
from src.apps.custom_view import BaseView


class Userauthorization(BaseView):
    """Авторизация пользователя"""

    login_required = False

    def get(self, request):
        form = AuthorizationForm()
        return render(
            request,
            "auth.html",
            {"form": form},
        )

    def post(self, request):
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = authenticate(
                    request, username=cd["email"], password=cd["password"]
                )
                if user and user.is_active:
                    login(request, user)
                    next_url = request.GET.get(REDIRECT_FIELD_NAME, '/default-url/')
                    return redirect(next_url)
                else:
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "Неверный логин или пароль.",
                        },
                        status=400,
                    )
            except IntegrityError:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Такого email не существует",
                    },
                    status=404,
                )
