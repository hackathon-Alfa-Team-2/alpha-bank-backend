from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser, Grade, Position, Role


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Учетные данные",
            {
                "fields": ("username", "password"),
            },
        ),
        (
            "Персональная информация",
            {"fields": ("first_name", "last_name", "email")},
        ),
        (
            "Права доступа",
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
        (
            "Компетенции",
            {
                "fields": ("role", "position", "grade"),
            },
        ),
    )
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "second_name",
        "is_supervisor",
        "grade",
        "position",
        "supervisor",
    )
    list_filter = ("role", "grade", "position")
    list_display_links = (
        "id",
        "username",
        "first_name",
        "last_name",
    )
    search_fields = ("first_name", "last_name")

    @admin.display(description="Руководитель", boolean=True)
    def is_supervisor(self, user: CustomUser):
        return user.is_supervisor


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


admin.site.unregister(Group)
