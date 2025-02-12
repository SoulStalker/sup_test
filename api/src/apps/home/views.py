from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
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
        user = request.user
        #список задач за которые ответсвенный
        task_responsible = self.task_service.get_list_responsible(user_id=user.id)
        #список задач у который автор
        task_contributor = self.task_service.get_list_contributor(user_id=user.id)
        #количество завершённых задач
        task_success = len(tuple(filter(lambda x: x.status == 'Готов', task_contributor)))
        #колиество задач
        quantity_task_responsible = len(task_responsible)
        #список проектов в которых участник
        projects_participants = self.project_service.get_list_participants(user_id=user.id)
        #количество завершённых проектов
        projects_success = len(tuple(filter(lambda x: x.status == 'В поддержке', projects_participants)))
        #количество активныз проектов
        projects_active = len(tuple(filter(lambda x: x.status in ('В обсуждении', 'В разработке'), projects_participants)))

        
        context = {
                'user': user,
                'task_responsible': task_responsible,
                'quantity_task_responsible': quantity_task_responsible,
                'task_success': task_success,
                'task_contributor': task_contributor,
                'projects_participants': projects_participants,
                'projects_success': projects_success,
                'projects_active': projects_active,
            }
        return render(request, 'home/home_lk.html', context)