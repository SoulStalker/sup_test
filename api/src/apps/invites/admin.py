from django.contrib import admin
from src.models.invites import Invite


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ("link", "status", "created_at", "expires_at")
    list_filter = ("status", "created_at", "expires_at")
    search_fields = ("link", "status", "created_at", "expires_at")
    readonly_fields = ("status", "created_at", "expires_at")
