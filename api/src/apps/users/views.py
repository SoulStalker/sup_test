from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from src.apps.users.forms import CustomUserForm, ListUserForm
from src.models.users import CustomUser, CustomUserList
from validators.validators import ModelValidator


class UserLogin(TemplateView, CustomUserForm):
    """Представление для авторизации пользователя."""

    template_name = "index.html"
    success_url = reverse_lazy("login")
    form_class = CustomUserForm
    success_message = "Вы успешно вошли."


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    """Представление для изменения пароля пользователю."""

    template_name = "password.html"
    success_url = reverse_lazy("user_list")

    def post(self, request, *args, **kwargs):
        old_password: str = request.POST.get("old_password")
        new_password1: str = request.POST.get("new_password1")
        new_password2: str = request.POST.get("new_password2")

        user: CustomUser = request.user

        if not user.check_password(old_password):
            messages.error(request, "Неверный пароль")
            return redirect("password")

        if len(new_password1) < 8:
            messages.error(
                request, "Пароль должен содержать минимум 8 символов."
            )
            return redirect("password")

        if new_password1 == old_password:
            messages.error(
                request, "Новый пароль не может совпадать с предыдущим."
            )
            return redirect("password")

        if new_password1 != new_password2:
            messages.error(request, "Пароли должны совпадать.")
            return redirect("password")

        try:
            ModelValidator.validate_password(new_password1)
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect("password")

        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Пароль успешно изменен.")
        return redirect("user_list")


class SignUpView(CreateView):
    """Представление для создания пользователя."""

    template_name = "reg.html"
    success_url = reverse_lazy("user_list")
    form_class = CustomUserForm
    success_message = "Профиль был успешно создан."


class UserListView(ListView):
    """Представление для просмотра списка пользователей с фильтрацией по ролям ."""

    model = CustomUserList
    paginate_by = 50
    template_name = "UserTable.html"
    context_object_name = "users"

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.GET.get("role")
        if role:
            queryset = queryset.filter(role=role)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter-form"] = ListUserForm(self.request.GET)
        return context
