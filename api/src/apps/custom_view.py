from django.http import HttpResponse, HttpResponseNotAllowed
from src.apps.meets.repository import CategoryRepository, MeetsRepository
from src.apps.users.repository import (
    PermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.domain.meet.service import MeetCategoryService, MeetService
from src.domain.user.service import PermissionService, RoleService, UserService


class BaseView:
    """
    Базовый класс для кастомных контроллеров вместо контроллеров джанги
    дополнительные передаваемые параметры идут в kwargs
    """

    category_service = MeetCategoryService(CategoryRepository())
    meet_service = MeetService(MeetsRepository(), CategoryRepository())
    user_service = UserService(UserRepository())
    role_service = RoleService(RoleRepository())
    permission_service = PermissionService(PermissionRepository())

    http_method_names = ["get", "post", "put", "patch", "delete"]
    # Определяем, требуется ли аутентификация
    login_required = True

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def as_view(cls):
        # Создаем метод as_view для интеграции с Django
        def view(request, *args, **kwargs):
            self = cls(request, *args, **kwargs)
            return self.dispatch()

        return view

    def dispatch(self):
        # Проверка авторизации
        if self.login_required and not self.request.user.is_authenticated:
            # todo add redirect to login page
            return HttpResponse("Залогинься")

        # Определяет возможность использования передаваемого метода
        method = getattr(self, self.request.method.lower(), None)
        if not method or not callable(method):
            return HttpResponseNotAllowed(self._get_allowed_methods())

        return method(self.request, *self.args, **self.kwargs)

    def _get_allowed_methods(self):
        # Получение доступных методов
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]
