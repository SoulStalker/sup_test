from django.contrib import admin
from src.models.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
