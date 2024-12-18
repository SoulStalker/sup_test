from django.contrib.auth.views import redirect_to_login
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.http import HttpResponseNotAllowed, JsonResponse
from src.apps.invites.repository import InviteRepository
from src.apps.meets.repository import CategoryRepository, MeetsRepository
from src.apps.projects.repository import FeaturesRepository, ProjectRepository
from src.apps.teams.repository import TeamRepository
from src.apps.users.repository import (
    PermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.domain.invites.service import InviteService
from src.domain.meet.service import MeetCategoryService, MeetService
from src.domain.project.service import FeatureService, ProjectService
from src.domain.teams.service import TeamService
from src.domain.user.service import PermissionService, RoleService, UserService


class BaseView:
    """
    Базовый класс для кастомных контроллеров вместо контроллеров джанги
    дополнительные передаваемые параметры идут в kwargs
    """

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    # Сервисы приложений
    category_service = MeetCategoryService(repository=CategoryRepository())
    meet_service = MeetService(
        repository=MeetsRepository(), category_repository=CategoryRepository()
    )
    invite_service = InviteService(InviteRepository())
    project_service = ProjectService(ProjectRepository())
    features_service = FeatureService(FeaturesRepository())
    user_service = UserService(UserRepository())
    role_service = RoleService(RoleRepository())
    permission_service = PermissionService(PermissionRepository())
    team_service = TeamService(TeamRepository())

    # Разрешенные методы
    http_method_names = ["get", "post", "put", "patch", "delete"]
    # Определяем, требуется ли аутентификация
    login_required = True
    # Параметры пагинации по умолчанию
    items_per_page = 50
    page_param = "page"
    per_page = "per_page"

    def paginate_queryset(self, queryset):
        """
        Метод для пагинации
        """
        per_page = self.request.GET.get(self.per_page, self.items_per_page)
        try:
            per_page = int(per_page)
        except (TypeError, ValueError):
            return queryset

        paginator = Paginator(queryset, per_page)
        page = self.request.GET.get(self.page_param, 1)

        try:
            paginated_items = paginator.page(page)
        except PageNotAnInteger:
            paginated_items = paginator.page(1)
        except EmptyPage:
            paginated_items = paginator.page(paginator.num_pages)

        return paginated_items

    @classmethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            self = cls(request, *args, **kwargs)
            return self.dispatch()

        return view

    def dispatch(self):
        if self.login_required and not self.request.user.is_authenticated:
            # Перенаправление на страницу авторизации
            return redirect_to_login(self.request, login_url="/admin/")

        method = getattr(self, self.request.method.lower(), None)
        if not method or not callable(method):
            return HttpResponseNotAllowed(self._get_allowed_methods())

        return method(self.request, *self.args, **self.kwargs)

    def _get_allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

    @classmethod
    def handle_form(cls, form, save_method, *args, **kwargs):
        """
        Универсальная обработка форм.
        - form: объект формы.
        - save_method: метод для сохранения данных (например, self.meet_service.create).
        - *args, **kwargs: аргументы для save_method.
        """
        if form.is_valid():
            try:
                result, err = save_method(*args, **kwargs)

                print(result, err)

                if isinstance(result, dict) and result.get(
                    "error"
                ):  # Допустим, сервис может вернуть ошибку
                    return JsonResponse(
                        {"status": "error", "message": result["error"]},
                        status=400,
                    )
                return JsonResponse({"status": "success"}, status=201)
            except IntegrityError as e:
                return JsonResponse(
                    {"status": "error", "message": str(e)}, status=400
                )
        return JsonResponse(
            {"status": "error", "errors": form.errors}, status=400
        )
