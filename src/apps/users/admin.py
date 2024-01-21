from django.contrib import admin

from .models import CustomUser, Grade, Position, Role


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "second_name",
        "role",
        "grade",
        "position",
        "supervisor",
    )
    list_filter = ("role", "grade", "position")
    list_display_links = (
        "id",
        "first_name",
        "last_name",
    )
    search_fields = ("first_name", "last_name")


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
