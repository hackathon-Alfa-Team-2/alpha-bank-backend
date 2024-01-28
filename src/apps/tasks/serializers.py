from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "description",
            "deadline",
            "status",
            "date_added",
            "lms_id",
        )
        read_only_fields = ("id", "date_added", "lms_id")

    def validate_name(self, name):
        lms_id = self.context["request"].parser_context["kwargs"]["lms_id"]
        name_exists = Task.objects.filter(name=name, lms_id=lms_id).exists()
        if name_exists:
            raise ValidationError(f'Задача с именем "{name}" уже существует.')
        return name

    def validate(self, attrs):
        lms_id = self.context["request"].parser_context["kwargs"]["lms_id"]
        attrs["lms_id"] = lms_id
        return attrs

    def validate_deadline(self, value):
        if timezone.now().date() >= value:
            raise serializers.ValidationError(
                "Дата дэдлайна не может быть раньше даты создания"
            )
        return value
