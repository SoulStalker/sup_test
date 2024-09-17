from django.contrib import admin

from apps.users.models import CustomUser, Permissions, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    search_fields = ("name",)


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "description")
    search_fields = ("name", "code")


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
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
        ("Role and Status", {"fields": ("role", "is_active", "is_admin")}),
    )
