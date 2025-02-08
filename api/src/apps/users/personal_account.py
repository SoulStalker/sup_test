from django.shortcuts import render
from django.urls import reverse
from src.apps.custom_view import BaseView





class PersonalAccount(BaseView):
    '''Личный кабинет'''

    def get(self, request, *args, **kwargs):
        user = request.user
        #список задач за которые ответсвенный
        task_responsible = self.task_service.get_list_responsible(user_id=user.id)
        #список задач у который автор
        task_contributor = self.task_service.get_list_contributor(user_id=user.id)\
        #количество завершённых задач
        task_success = len(tuple(filter(lambda x: x.status == 'Готов', task_contributor)))
        #список проектов в которых участник
        projects_participants = self.project_service.get_list_participants(user_id=user.id)
        personal_account_url = reverse("users:personal_account")
        
        context = {
                'user': user,
                'task_responsible': task_responsible,
                'task_success': task_success,
                'task_contributor': task_contributor,
                'projects_participants': projects_participants,
                'personal_account_url': personal_account_url,
            }
  
        return render(self.request, "personal_account.html", context)