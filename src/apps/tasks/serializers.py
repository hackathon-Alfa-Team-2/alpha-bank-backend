from rest_framework import serializers

from src.apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="name")
    description = serializers.CharField(max_length=512)
    deadline = serializers.DateField(read_only=True)
    date_added = serializers.DateField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "deadline",
            "status",
            "date_added",
            "lms",
        ]

    def get_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user
