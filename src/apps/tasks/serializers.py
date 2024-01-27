from rest_framework import serializers

from src.apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
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
