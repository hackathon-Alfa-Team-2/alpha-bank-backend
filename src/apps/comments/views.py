from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.apps.comments.models import Comment
from src.apps.comments.serializers import CommentSerializer
from src.apps.tasks.models import Task
from src.base.permissions import IsAdminOrRelatedToTask


class CommentViewSet(ModelViewSet):
    """Представление комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAdminOrRelatedToTask)

    def get_queryset(self):
        return Comment.objects.select_related("comment_author").filter(
            task_id=self.kwargs.get("task_id")
        )

    def list(self, request, *args, **kwargs):
        task_id = kwargs.get("task_id")
        user = self.request.user
        task = Task.objects.select_related("lms").filter(
            Q(id=task_id, lms__employee=user)
            | Q(id=task_id, lms__supervisor=user)
        )
        if not task:
            return Response(
                data={
                    "detail": "You are not allowed to read a comment on a "
                    "task that you are not related to"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().list(request, *args, **kwargs)
