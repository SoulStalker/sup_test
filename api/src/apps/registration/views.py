import re

from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.registration.forms import RegistrationForm
from src.domain.registration.dtos import RegistrationDTO


class UserRegistration(BaseView):
    """Регистрация пользователя"""

    login_required = False

    def get(self, request, invitation_code):
        self.registration_service.chek_invitation_code_or_404(invitation_code)
        form = RegistrationForm()
        return render(
            request,
            "reg.html",
            {"form": form},
        )

    def post(self, request, invitation_code):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                err = self.registration_service.create(
                    RegistrationDTO(
                        name=form.cleaned_data["name"],
                        surname=form.cleaned_data["surname"],
                        email=form.cleaned_data["email"],
                        password1=form.cleaned_data["password1"],
                        password2=form.cleaned_data["password2"],
                        tg_name=form.cleaned_data["tg_name"],
                        tg_nickname=form.cleaned_data["tg_nickname"],
                        google_meet_nickname=form.cleaned_data[
                            "google_meet_nickname"
                            ],
                        gitlab_nickname=form.cleaned_data["gitlab_nickname"],
                        github_nickname=form.cleaned_data["github_nickname"],
                        role_id=None,
                        permissions_ids=[],
                        team_id=None,
                        date_joined=None,
                )
                    )
                if err:
                    return JsonResponse(
                        {"status": "error", "message": str(err)}, status=400
                    )
                invite_DTO = self.invite_service.create_invite_dto(
                    invitation_code
                    )
                self.invite_service.update_status(invite_DTO, status = 'USED')
                self.verifyemail_service.create(
                    email=form.cleaned_data["email"],
                    name=form.cleaned_data["name"]
                    )
                return JsonResponse({"status": "success"}, status=201)
            
            except IntegrityError as err:
                matches = re.findall(r"\((.*?)\)", str(err))
                return JsonResponse(
                    {
                        "status": "error",
                        "message": f"Такой {matches[0]} уже существует",
                    },
                    status=400,
                )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
            )