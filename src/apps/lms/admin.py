from django import forms
from django.contrib import admin, messages

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

    def save_model(self, request, obj, form, change):
        employee = obj.employee
        supervisor = obj.supervisor
        if employee.supervisor != supervisor:
            messages.error(
                request,
                f"ИПР {obj.name} не создан. "
                f"Сотрудник должен быть подчинен указанному руководителю.",
            )

        else:
            super().save_model(request, obj, form, change)
