from django.shortcuts import render
from src.apps.custom_view import BaseView





class PersonalAccount(BaseView):
    '''Личный кабинет'''

    def get(self, request, *args, **kwargs):
        user = request.user
        #список за что ответсвенный
        task_responsible = self.task_service.get_list_responsible(user_id=user.id)
        #список у каких задач автор
        task_contributor = self.task_service.get_list_contributor(user_id=user.id)
        context = {
                'user': user,
                'task_responsible': task_responsible,
                'task_contributor': task_contributor,
            }
  
        return render(self.request, "personal_account.html", context)