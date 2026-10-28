from django.contrib import admin
from practice.models import PracticeExercise, PracticeResult


@admin.register(PracticeExercise)
class PracticeExerciseAdmin(admin.ModelAdmin):
    list_display = ("chapter", "difficulty", "user", "created_at")
    list_filter = ("chapter", "difficulty", "created_at")
    search_fields = ("question", "user__username")


@admin.register(PracticeResult)
class PracticeResultAdmin(admin.ModelAdmin):
    list_display = ("exercise", "user", "chapter", "score", "created_at")
    list_filter = ("chapter", "score", "created_at")
    search_fields = ("user__username", "feedback")
