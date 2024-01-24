from rest_framework.viewsets import ModelViewSet

from src.apps.comments.models import Comment
from src.apps.comments.serializers import CommentSerializer
from src.base.permissions import IsAdminOrSupervisorOrTaskExecutor


class CommentViewSet(ModelViewSet):
    """Представление комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrSupervisorOrTaskExecutor,)

    def get_queryset(self):
        return Comment.objects.filter(id=self.kwargs.get("pk"))
