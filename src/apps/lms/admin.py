from django import forms
from django.contrib import admin
from django.utils import timezone

from src.apps.lms.models import LMS
from src.apps.users.models import CustomUser


class LMSAdminForm(forms.ModelForm):
    class Meta:
        model = LMS
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["employee"].queryset = CustomUser.objects.filter(
            role__name="employee"
        )
        self.fields["supervisor"].queryset = CustomUser.objects.filter(
            role__name="supervisor"
        )

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline <= timezone.now().date():
            raise forms.ValidationError("Deadline должен быть в будущем.")
        return self.cleaned_data["deadline"]

    def clean(self):
        data = super().clean()
        employee = data.get("employee")
        supervisor = data.get("supervisor")
        if employee.supervisor != supervisor:
            raise forms.ValidationError(
                "Сотрудник должен быть подчинен указанному руководителю."
            )
        return data


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
    form = LMSAdminForm
    list_display_links = "id", "name"
    list_editable = "status", "is_active", "deadline"
    search_fields = "name", "employee__last_name"
    search_help_text = "Поиск по названию ИПР или фамилии сотрудника."
