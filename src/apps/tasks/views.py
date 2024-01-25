from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from serializers import TaskSerializer

from tasks.models import Task
from base.permissions import IsAdminOrSupervisorOrTaskExecutor


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdminOrSupervisorOrTaskExecutor,
    )
