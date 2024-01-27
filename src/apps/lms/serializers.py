from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.apps.lms.models import LMS
from src.apps.tasks.serializers import TaskSerializer


class ShortDataLMSSerializer(serializers.ModelSerializer):
    """
    Сериализатор c именем, датой, статусом ИПР.
    """

    class Meta:
        model = LMS
        fields = (
            "name",
            "deadline",
            "status",
        )
        read_only_fields = ("__all__",)


class FullDataLMSSerializer(serializers.ModelSerializer):
    """
    Сериализатор ИПР со всеми данными включая список задач.
    """

    tasks = TaskSerializer(many=True, read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = LMS
        fields = (
            "id",
            "name",
            "description",
            "is_active",
            "deadline",
            "status",
            "tasks",
            "skill_assessment_before",
            "skill_assessment_after",
            "employee_id",
            "supervisor",
        )
        read_only_fields = ("supervisor", "employee_id")

    def validate_name(self, name):
        employee_id = self.context["request"].parser_context["kwargs"][
            "user_id"
        ]
        supervisor = self.context["request"].user
        name_lms_exists = LMS.objects.filter(
            supervisor_id=supervisor.id,
            employee_id=employee_id,
            name=name,
        ).exists()
        if name_lms_exists:
            raise ValidationError(
                f'У сотрудника уже есть ИПР с именем "{name}"'
            )
        return name

    def validate_is_active(self, is_active):
        if is_active:
            employee_id = self.context["request"].parser_context["kwargs"][
                "user_id"
            ]
            if LMS.objects.filter(
                employee_id=employee_id,
                is_active=True,
            ).exists():
                raise ValidationError("У сотрудника уже есть активный ИПР.")
        return is_active

    def validate(self, data):
        employee_id = self.context["request"].parser_context["kwargs"][
            "user_id"
        ]
        supervisor = self.context["request"].user
        data["employee_id"] = employee_id
        data["supervisor"] = supervisor
        return data
