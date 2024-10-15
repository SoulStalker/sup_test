from django.http import HttpResponseNotAllowed


class BaseView:
    """
    Базовый класс для кастомных контроллеров вместо контроллеров джанги
    дополнительные передаваемые параметры идут в kwargs
    """
    http_method_names = ["get", "post", "put", "patch", "delete"]

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
        # Определяет возможность использования передаваемого метода
        # и вызывает передаваемой метод из класса
        method = getattr(self, self.request.method.lower(), None)
        if not method or not callable(method):
            return HttpResponseNotAllowed(self._get_allowed_methods())
        
        return method(self.request, *self.args, **self.kwargs)

    def _get_allowed_methods(self):
        # Получение доступных методов
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]
        