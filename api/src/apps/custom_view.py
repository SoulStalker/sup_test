from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseNotAllowed
from src.apps.invites.repository import InviteRepository
from src.apps.meets.repository import CategoryRepository, MeetsRepository
from src.apps.projects.repository import FeaturesRepository, ProjectRepository
from src.apps.users.repository import UserRepository
from src.domain.invites.service import InviteService
from src.domain.meet.service import MeetCategoryService, MeetService
from src.domain.user.service import UserService
from src.domain.project.service import FeatureService, ProjectService


class BaseView:
    """
    Базовый класс для кастомных контроллеров вместо контроллеров джанги
    дополнительные передаваемые параметры идут в kwargs
    """

    category_service = MeetCategoryService(CategoryRepository())
    meet_service = MeetService(MeetsRepository(), CategoryRepository())
    invite_service = InviteService(InviteRepository())

    project_service = ProjectService(ProjectRepository())
    features_service = FeatureService(FeaturesRepository())
    user_service = UserService(UserRepository())

    http_method_names = ["get", "post", "put", "patch", "delete"]
    # Определяем, требуется ли аутентификация
    login_required = True
    # Параметры пагинации по умолчанию
    items_per_page = 10
    page_param = "page"

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def paginate_queryset(self, queryset):
        """
        Метод для пагинации queryset
        """
        paginator = Paginator(queryset, self.items_per_page)
        page = self.request.GET.get(self.page_param, 1)

        try:
            paginated_items = paginator.page(page)
        except PageNotAnInteger:
            paginated_items = paginator.page(1)
        except EmptyPage:
            paginated_items = paginator.page(paginator.num_pages)

        return {
            "items": paginated_items,
            "paginator": paginator,
            "current_page": paginated_items.number,
            "total_pages": paginator.num_pages,
            "has_next": paginated_items.has_next(),
            "has_previous": paginated_items.has_previous(),
            "page_range": paginator.page_range,
        }

    @classmethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            self = cls(request, *args, **kwargs)
            return self.dispatch()

        return view

    def dispatch(self):
        if self.login_required and not self.request.user.is_authenticated:
            return HttpResponse("Залогинься")

        method = getattr(self, self.request.method.lower(), None)
        if not method or not callable(method):
            return HttpResponseNotAllowed(self._get_allowed_methods())

        return method(self.request, *self.args, **self.kwargs)

    def _get_allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]
