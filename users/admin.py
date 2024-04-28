from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User


@admin.register(User)
class AdminUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("channel_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_member", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    list_display = ("username", "channel_name", "is_member", "last_login")
    search_fields = ("username", "channel_name", "email")
    filter_horizontal = ("groups", "user_permissions")

