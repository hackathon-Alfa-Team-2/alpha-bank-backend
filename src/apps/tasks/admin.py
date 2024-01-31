from django import forms
from django.contrib import admin
from django.utils import timezone

from src.apps.tasks.models import Task


class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline <= timezone.now().date():
            raise forms.ValidationError("Deadline должен быть в будущем.")
        return self.cleaned_data["deadline"]


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
    form = TaskAdminForm
    list_display_links = "id", "name"
    list_editable = ("status",)
    search_fields = "name", "employee__name"
    search_help_text = "Поиск по названию ИПР или задаче"
