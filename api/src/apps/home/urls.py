from django.urls import path
from .views import HomeView
app_name = 'home'  # Определение app_name

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),  # Пример маршрута
    # Другие маршруты
]