from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from serializers import TaskSerializer

from tasks.models import Task
from base.permissions import IsAdminOrSupervisorOrTaskExecutor


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdminOrSupervisorOrTaskExecutor,
    )

    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        queryset = Task.objects.filter(id=task_id)
        return queryset
