from rest_framework import viewsets
from serializers import TaskSerializer

from tasks.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        # в работе
        serializer.save()

    def perform_update(self, serializer):
        # в работе
        serializer.save()

    def perform_destroy(self, instance):
        # в работе
        instance.delete()
