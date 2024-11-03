from pprint import pprint

from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView


class InvitesView(BaseView):
    def get(self, *args, **kwargs):
        invites = self.invite_service.get_invites_list()
        context = {"invites": invites}
        return render(self.request, "invites.html", context)

    def post(self, *args, **kwargs):
        pprint("0. InvitesView.post")

        # todo добавить ответ в случае ошибки или успеха
        invite = self.invite_service.create()

        pprint(invite)

        return JsonResponse({"invite": invite})

    def delete(self, *args, **kwargs):
        invite = self.invite_service.delete(self.request.data["id"])
        return JsonResponse({"invite": invite})
