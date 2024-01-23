from rest_framework import viewsets
from rest_framework import viewsets
from serializers import TaskSerializer

from tasks.models import Task
from base.permissions import IsAdminOrSupervisorOrTaskExecutor


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAdminOrSupervisorOrTaskExecutor,)

    http_method_names = (
        "get",
        "post",
        "put",
        "patch",
        "delete",
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
