from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from src.apps.comments.models import Comment
from src.apps.comments.serializers import CommentSerializer
from src.base.permissions import IsAdminOrRelatedToTask


class CommentViewSet(ModelViewSet):
    """Представление комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAdminOrRelatedToTask)

    def get_queryset(self):
        return Comment.objects.select_related("comment_author").filter(
            task_id=self.kwargs.get("task_id")
        )
