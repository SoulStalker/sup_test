from django.contrib.auth import (
    REDIRECT_FIELD_NAME,
    authenticate,
    login,
    logout,
)
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from src.apps.authorization.forms import AuthorizationForm
from src.apps.custom_view import BaseView


class UserAuthorization(BaseView):
    """Авторизация пользователя"""

    login_required = False

    def get(self, request):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("authorization:logout"))
        form = AuthorizationForm()
        return render(request, "auth.html", {"form": form})

    def post(self, request):
        form = AuthorizationForm(request.POST)
        next_url = request.GET.get(
            REDIRECT_FIELD_NAME, "/").replace('/authorization/logout/', '/'
                                )
        error_message = None
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = authenticate(
                    request, username=cd["email"], password=cd["password"]
                )
                if user and user.is_active:
                    login(request, user)
                    return redirect(next_url)
                else:
                    error_message = "Неверный логин или пароль."
            except IntegrityError:
                error_message = "Неверный логин или пароль."
        return render(request, "auth.html", {"form": form, "error_message": error_message})


class UserLogout(BaseView):

    def get(self, request):
        return render(request, "logout.html")

    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("authorization:logout"))
