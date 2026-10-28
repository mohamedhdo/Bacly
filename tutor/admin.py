from django.contrib import admin
from tutor.models import TutorSession, TutorMessage


class TutorMessageInline(admin.TabularInline):
    model = TutorMessage
    extra = 0


@admin.register(TutorSession)
class TutorSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "chapter", "summary", "had_mistake", "created_at")
    list_filter = ("chapter", "had_mistake", "created_at")
    search_fields = ("user__username", "summary", "input_text")
    inlines = [TutorMessageInline]


@admin.register(TutorMessage)
class TutorMessageAdmin(admin.ModelAdmin):
    list_display = ("session", "role", "content", "created_at")
    list_filter = ("role", "created_at")
