from django.shortcuts import render
from django.http import HttpResponse
from src.apps.custom_view import BaseView

class HomeView(BaseView):
    def get(self, request):
        login_required = False


        return render(request, 'home/home.html')