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

    class Meta:
        model = LMS
        fields = (
            "name",
            "description",
            "is_active",
            "deadline",
            "status",
            "tasks",
            "skill_assessment_before",
            "skill_assessment_after",
            "employee",
            "supervisor",
        )
        read_only_fields = (
            "is_active",
            "supervisor",
        )

    def validate(self, data):
        employee = data["employee"]
        if LMS.objects.filter(employee=employee, is_active=True).exists():
            raise ValidationError("У сотрудника уже есть активный ИПР.")
        return data

    def create(self, validated_data):
        supervisor = validated_data.get("supervisor")
        employee = validated_data.get("employee")
        if supervisor == employee:
            raise ValidationError(
                "Руководитель не может назначить исполнителем самого себя."
            )
        return super().create(validated_data)
