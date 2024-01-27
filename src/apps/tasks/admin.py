from django.contrib import admin

from src.apps.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "deadline",
        "status",
        "date_added",
        "lms",
    )
    list_display_links = "id", "name"
    list_editable = "status", "deadline"
    search_fields = "name", "employee__name"
    search_help_text = "Поиск по названию ИПР или задачи."
