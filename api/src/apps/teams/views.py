from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from src.apps.custom_view import BaseView
from src.apps.teams.forms import CreateTeamForm
from src.domain.teams.dtos import CreateTeamDTO

User = get_user_model()


class TeamListView(BaseView):
    def get(self, *args, **kwargs):
        teams = self.team_service.get_team_list()
        teams = self.paginate_queryset(teams)
        users = User.objects.filter(team__isnull=True).distinct()
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
            participants = request.POST.getlist("participants")

            print(participants)
            print(type(participants))
            # participants = [int(i) for i in participants]
            team_dto = CreateTeamDTO(
                name=form.cleaned_data["name"],
                participants=participants,
            )

            try:
                # Создание команды
                team = self.team_service.create(team_dto)

                print(team)

                # Возвращаем успешный ответ с данными о созданнай команде
                return JsonResponse(
                    {
                        "status": "success",
                        "project": {
                            "name": team.name,
                            "participants": team.participants,
                        },
                    },
                    status=201,
                )

            except Exception as e:

                print(e)

                return JsonResponse(
                    {"status": "error", "message": str(e)}, status=400
                )

        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )


class TeamUpdateView(BaseView):
    def get(self, *args, **kwargs):
        team_id = kwargs.get("pk")
        team = self.team_service.get_team(team_id)

        users = User.objects.order_by("id")

        return render(
            self.request,
            "teams/team_update.html",
            {"team": team, "users": users},
        )
