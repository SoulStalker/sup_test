from django.http import Http404


class AdminPermission:
    def has_permission(self, request, view):
        return request.user.role == "teamlead"

    def dispatch(self):
        if not self.has_permission(self.request, self):
            raise Http404()
        return super().dispatch(self)
