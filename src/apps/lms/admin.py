from django.contrib import admin


from src.apps.lms.models import LMS


@admin.register(LMS)
class LMSAdmin(admin.ModelAdmin):
    """Админ панель для модели ИПР."""

    list_display = (
        "id",
        "name",
        "is_active",
        "deadline",
        "status",
        "employee",
        "supervisor",
        "date_added",
    )
    list_display_links = ("id", "name")
    list_editable = "status", "is_active", "deadline"
    search_fields = "name", "employee__last_name"
    search_help_text = "Поиск по названию ИПР или фамилии сотрудника."
