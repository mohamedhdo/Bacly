from django.contrib import admin
from core.models import AiCallLog


@admin.register(AiCallLog)
class AiCallLogAdmin(admin.ModelAdmin):
    list_display = ("user", "feature", "created_at")
    list_filter = ("feature", "created_at")
    search_fields = ("user__username",)
