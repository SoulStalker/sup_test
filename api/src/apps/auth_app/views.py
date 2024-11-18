from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import LoginForm

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/meets/")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user:
                if not user.is_active:
                    return HttpResponse(
                        "Вам нужно активировать аккаунт по ссылке из email."
                    )
                login(request, user)
                return redirect(
                    # todo заменить на ссылку профиля
                    "/meets/"
                )
            else:
                return HttpResponse("Email или пароль не верен")
    else:
        form = LoginForm()

    return render(request, "auth_app/login.html", {"form": form})


def logout_view(request):
    return render(request, "auth_app/logout.html")
