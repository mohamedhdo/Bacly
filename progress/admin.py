from django.contrib import admin
from progress.models import StudyPlan, Activity


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ("user", "week_start", "created_at")
    list_filter = ("week_start",)
    search_fields = ("user__username",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "activity_type", "created_at")
    list_filter = ("date", "activity_type")
    search_fields = ("user__username", "description")
