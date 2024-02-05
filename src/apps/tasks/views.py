from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from config.settings import CACHE_MIDDLEWARE_SECONDS
from src.apps.tasks.models import Task
from src.apps.tasks.serializers import TaskSerializer
from src.base.permissions import IsAdminOrSupervisorOrTaskExecutor


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdminOrSupervisorOrTaskExecutor,
    )
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    swagger_tags = ["Tasks"]

    def get_queryset(self):
        queryset = Task.objects.select_related("lms").filter(
            lms_id=self.kwargs.get("lms_id"),
            lms__employee=self.kwargs.get("user_id"),
        )
        return queryset

    @method_decorator(cache_page(CACHE_MIDDLEWARE_SECONDS))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_MIDDLEWARE_SECONDS))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
