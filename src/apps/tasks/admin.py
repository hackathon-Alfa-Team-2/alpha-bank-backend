from django.contrib import admin

from src.apps.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "formatted_deadline",
        "status",
        "date_added",
        "lms",
    )
    list_display_links = "id", "name"
    list_editable = ("status",)
    search_fields = "name", "employee__name"
    search_help_text = "Поиск по названию ИПР или задачи."

    def formatted_deadline(self, obj):
        # Используем strftime для форматирования даты в строку
        return obj.deadline.strftime("%Y-%m-%d") if obj.deadline else None

    formatted_deadline.short_description = "Formatted Deadline"
