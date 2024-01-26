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

    def validate(self, attrs):
        task_id = (
            self.context["request"].parser_context["kwargs"].get("task_id")
        )
        user = self.context["request"].user
        attrs["task_id"] = task_id
        attrs["user"] = user
        return attrs
