from django.contrib import admin
from classes.models import SchoolClass


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ("name", "join_code", "teacher", "created_at")
    search_fields = ("name", "join_code", "teacher__username")
