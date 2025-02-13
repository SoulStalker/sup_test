from django.urls import path
from .views import HomeView, KanbanView, HomeLKView
app_name = 'home'  # Определение app_name

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('kanban/', KanbanView.as_view(), name='kanban_view'),
    path('lk/', HomeLKView.as_view(), name='home_lk_view'),
]