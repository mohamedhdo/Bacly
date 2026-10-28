from django.contrib import admin
from exams.models import Exam


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("user", "duration_minutes", "status", "total_grade", "started_at", "submitted_at")
    list_filter = ("status", "started_at")
    search_fields = ("user__username",)
