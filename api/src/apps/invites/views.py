from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView


class InvitesView(BaseView):
    def get(self):
        invites = self.invite_service.get_invites_list()
        context = {"invites": invites}
        return render(self.request, "invites.html", context)

    def post(self):
        invite = self.invite_service.create(self.request.data)
        return JsonResponse({"invite": invite})

    def delete(self):
        invite = self.invite_service.delete(self.request.data["id"])
        return JsonResponse({"invite": invite})
