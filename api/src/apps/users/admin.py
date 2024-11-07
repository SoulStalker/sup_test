from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from src.models.models import CustomUser, Permission, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    search_fields = ("name",)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "description")
    search_fields = ("name", "code")


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "name",
        "surname",
        "email",
        "tg_name",
        "tg_nickname",
        "google_meet_nickname",
        "gitlab_nickname",
        "github_nickname",
        "role",
        "is_active",
        "is_admin",
    )
    search_fields = ("name", "surname", "email", "tg_name", "tg_nickname")
    list_filter = ("role", "is_active", "is_admin")
    fieldsets = (
        (None, {"fields": ("name", "surname", "email", "password")}),
        ("Telegram", {"fields": ("tg_name", "tg_nickname")}),
        (
            "Nicknames",
            {
                "fields": (
                    "google_meet_nickname",
                    "gitlab_nickname",
                    "github_nickname",
                )
            },
        ),
        ("Avatar", {"fields": ("avatar",)}),
        (
            "Role and Status",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "surname",
                    "tg_name",
                    "tg_nickname",
                    "google_meet_nickname",
                    "gitlab_nickname",
                    "github_nickname",
                    "avatar",
                    "role",
                    "is_active",
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    ordering = ("email",)
    filter_horizontal = ()
