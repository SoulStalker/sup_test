from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.domain.invites.dtos import InviteDTO


class InvitesView(BaseView):
    def get(self, *args, **kwargs):
        invites = self.invite_service.get_invites_list()
        for invite in invites:
            self.invite_service.update_status(
                dto=InviteDTO(
                    pk=invite.pk,
                    link=invite.link,
                    status=invite.status,
                    created_at=invite.created_at,
                    expires_at=invite.expires_at,
                )
            )
        invites = self.invite_service.get_invites_list()
        invites = self.paginate_queryset(invites)
        context = {"invites": invites}
        return render(self.request, "invites_list.html", context)

    def post(self, *args, **kwargs):
        invite = self.invite_service.create()
        if invite:
            return JsonResponse({"message": "success"})

    def delete(self, *args, **kwargs):
        invite_id = kwargs.get("invite_id")
        try:
            self.invite_service.delete(invite_id)
            return JsonResponse(
                {"status": "success", "message": "Invite deleted"}
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=404
            )
