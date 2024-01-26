from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="name")
    description = serializers.CharField(max_length=512)
    deadline = serializers.DateField(required=True)

    class Meta:
        model = Task
        fields = ("__all__",)
        read_only_fields = (
            "id",
            "date_added",
        )
