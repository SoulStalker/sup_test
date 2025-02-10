from django.shortcuts import render
from django.http import HttpResponse
from src.apps.custom_view import BaseView

class HomeView(BaseView):
    login_required = False
    def get(self, request):


        return render(request, 'home/home.html')


class KanbanView(BaseView):
    def get(self, request):
        return render(request, 'kanban/kanban.html')

class HomeLKView(BaseView):
    def get(self, request):
        return render(request, 'home/home_lk.html')