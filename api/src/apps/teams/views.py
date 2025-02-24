from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.teams.forms import CreateTeamForm
from src.domain.teams import CreateTeamDTO, TeamDTO

User = get_user_model()


class TeamListView(BaseView):
    """Список команд"""

    def get(self, *args, **kwargs):
        teams = self.team_service.get_list()
        teams = self.paginate_queryset(teams)
        users = self.user_service.get_active_users()
        return render(
            self.request,
            "teams/teams_list.html",
            {"teams": teams, "users": users},
        )


class TeamCreateView(BaseView):
    def get(self, request, *args, **kwargs):
        form = CreateTeamForm(request.POST)

        return render(
            request,
            "create_team_modal.html",
            {
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            return self.handle_form(
                form,
                self.team_service.create,
                CreateTeamDTO(
                    name=form.cleaned_data["name"],
                    participants=form.cleaned_data["participants"],
                ),
                self.user_id,
            )
        print(form.errors)
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class TeamUpdateView(BaseView):
    def get(self, *args, **kwargs):
        team_id = kwargs.get("team_id")
        team, error = self.team_service.get_by_id(team_id, self.user_id)
        if error:
            return JsonResponse(
                {"status": "error", "message": error}, status=403
            )
        data = {
            "name": team.name,
            "participants": team.participants,
        }
        return JsonResponse(data)

    def post(self, *args, **kwargs):
        team_id = kwargs.get("team_id")
        form = CreateTeamForm(self.request.POST)
        if form.is_valid():
            return self.handle_form(
                form,
                self.team_service.update,
                team_id,
                TeamDTO(
                    id=team_id,
                    name=form.cleaned_data["name"],
                    participants=form.cleaned_data["participants"],
                ),
                self.user_id,
            )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class TeamDeleteView(BaseView):
    """
    Удаление команды
    """

    def delete(self, *args, **kwargs):
        team_id = kwargs.get("team_id")
        try:
            self.team_service.delete(pk=team_id, user_id=self.user_id)
            return JsonResponse(
                {"status": "success", "message": "Team deleted"}
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=404
            )
