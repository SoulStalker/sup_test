from django.contrib import admin
from src.models.verifyemail import VerifyEmail


@admin.register(VerifyEmail)
class VerifyEmailAdmin(admin.ModelAdmin):
    list_display = ("id", "link", "email", "created_at", "expires_at")
    list_filter = ("created_at", "expires_at")
    search_fields = ("link", "email", "created_at", "expires_at")
