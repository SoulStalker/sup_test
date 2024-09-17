from django.contrib import admin

from apps.meets.models import Category, Meet, MeetParticipant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)


class MeetParticipantInline(admin.TabularInline):
    model = MeetParticipant
    extra = 1


@admin.register(Meet)
class MeetAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_date", "start_time")
    list_display_links = ("title", "category", "start_time")
    search_fields = ("title", "category", "start_time", "end_time")
    inlines = [MeetParticipantInline]


@admin.register(MeetParticipant)
class MeetParticipantAdmin(admin.ModelAdmin):
    list_display = ("custom_user", "meet", "status")
    list_display_links = ("custom_user", "meet", "status")
    search_fields = ("custom_user", "meet")
