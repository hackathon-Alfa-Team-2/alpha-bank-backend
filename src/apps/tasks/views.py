from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.apps.tasks.models import Task
from src.apps.tasks.serializers import TaskSerializer
from src.base.permissions import IsAdminOrSupervisorOrTaskExecutor


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdminOrSupervisorOrTaskExecutor,
    )
    swagger_tags = ["Tasks"]

    def get_queryset(self):
        queryset = Task.objects.select_related("lms").filter(
            lms_id=self.kwargs.get("lms_id"),
            lms__employee=self.kwargs.get("user_id"),
        )
        return queryset
