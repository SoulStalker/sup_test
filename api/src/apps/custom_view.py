from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect
from src.apps.invites.repository import InviteRepository
from src.apps.meets.repository import CategoryRepository, MeetsRepository
from src.apps.projects.repository import (
    FeaturesRepository,
    ProjectRepository,
    TaskRepository,
    CommentRepository,
)
from src.apps.registration.repository import RegistarionRepository
from src.apps.teams.repository import TeamRepository
from src.apps.users.repository import (
    PermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.apps.verifyemail.repository import VerifyemailRepository
from src.domain.invites import InviteService
from src.domain.meet import MeetCategoryService, MeetService
from src.domain.project import (
    FeatureService,
    ProjectService,
    CommentService,
    TaskService,
)
from src.domain.registration.service import RegistrationService
from src.domain.teams import TeamService
from src.domain.user import PermissionService, RoleService, UserService
from src.domain.verifyemail.service import VerifyemailService


class BaseView:
    """
    Базовый класс для кастомных контроллеров вместо контроллеров джанги
    дополнительные передаваемые параметры идут в kwargs
    """

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user_id = request.user.id

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
    registration_service = RegistrationService(RegistarionRepository())
    verifyemail_service = VerifyemailService(VerifyemailRepository())
    task_service = TaskService(TaskRepository())
    comment_service = CommentService(CommentRepository())

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
            next_url = self.request.get_full_path()
            login_url = f"/authorization/?{REDIRECT_FIELD_NAME}={next_url}"
            return redirect(login_url)

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
        - save_method: метод для сохранения данных
        - *args, **kwargs: аргументы для save_method.
        """
        try:
            if not form.is_valid():
                return JsonResponse(
                    {"status": "error", "errors": form.errors}, status=400
                )

            result, err = save_method(*args, **kwargs)

            if err:
                return JsonResponse(
                    {"status": "error", "message": str(err)}, status=400
                )

            return JsonResponse({"status": "success"}, status=201)

        except IntegrityError as e:
            error_message = str(e)
            # Обработка дубликата заголовка
            if "meets_title_key" in error_message:
                return JsonResponse(
                    {
                        "status": "error",
                        "errors": {
                            "title": [
                                "Объект с таким названием уже существует"
                            ]
                        },
                    },
                    status=400,
                )
            # Здесь можно добавить обработку других уникальных ограничений

            # Для необработанных случаев возвращаем общее сообщение
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Ошибка сохранения: нарушение уникальности данных",
                },
                status=400,
            )

        except Exception as e:
            print(f"Unexpected error in handle_form: {str(e)}")
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Произошла внутренняя ошибка сервера",
                },
                status=500,
            )
