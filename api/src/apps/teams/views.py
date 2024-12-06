from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.teams.forms import CreateTeamForm
from src.domain.teams.dtos import CreateTeamDTO, TeamDTO

User = get_user_model()


class TeamListView(BaseView):
    def get(self, *args, **kwargs):
        teams = self.team_service.get_team_list()
        teams = self.paginate_queryset(teams)
        # users = User.objects.filter(team__isnull=True).distinct()
        users = self.user_service.get_user_list()
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
            team_dto = CreateTeamDTO(
                name=form.cleaned_data["name"],
                participants=form.cleaned_data["participants"],
            )
            try:
                # Создание команды
                team_dto, err = self.team_service.create(team_dto)
                if err:
                    return JsonResponse(
                        {"status": "error", "message": str(err)}, status=400
                    )
                return JsonResponse({"status": "success"}, status=201)
            except IntegrityError:
                return JsonResponse(
                    {"status": "error", "message": "Такой мит уже существует"},
                    status=400,
                )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class TeamUpdateView(BaseView):
    def get(self, *args, **kwargs):
        team_id = kwargs.get("team_id")
        team = self.team_service.get_team_by_id(team_id)
        data = {
            "name": team.name,
            "participants": team.participants,
        }
        return JsonResponse(data)

    def post(self, *args, **kwargs):
        team_id = kwargs.get("team_id")
        team = self.team_service.get_team_by_id(team_id)
        form = CreateTeamForm(self.request.POST)
        if form.is_valid():
            try:
                team_dto = TeamDTO(
                    id=team.id,
                    name=form.cleaned_data["name"],
                    participants=form.cleaned_data["participants"],
                )
                team_dto, err = self.team_service.update(team_dto)
                if err:
                    return JsonResponse(
                        {"status": "error", "message": str(err)}, status=400
                    )
            except Exception as err:
                print(err)
            return JsonResponse({"status": "success"}, status=201)
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
            self.team_service.delete(team_id=team_id)
            return JsonResponse(
                {"status": "success", "message": "Team deleted"}
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=404
            )
