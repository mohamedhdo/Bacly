from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "stream", "school_class", "is_staff")
    list_filter = ("role", "stream", "is_staff", "is_active")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Bacly Profile", {"fields": ("role", "stream", "bac_date", "school_class")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Bacly Profile", {"fields": ("role", "stream", "bac_date", "school_class")}),
    )
