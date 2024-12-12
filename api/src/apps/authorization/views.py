
from src.apps.custom_view import BaseView
from src.apps.authorization.forms import AuthorizationForm
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout



class Userauthorization(BaseView):
#     """Авторизация пользователя"""

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
            user = authenticate(
                request, username=cd['email'], password=cd['password']
                )
            if user and user.is_active:
                login(request, user)
                return JsonResponse(
                        {"status": "error", "message": 'Добро пожаловать'}, status=200
                    )