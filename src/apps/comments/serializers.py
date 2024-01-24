from rest_framework.serializers import ModelSerializer

from src.apps.comments.models import Comment


class CommentSerializer(ModelSerializer):
    """Сериализатор комментариев."""

    class Meta:
        model = Comment
        fields = (
            "id",
            "comment_author",
            "task",
            "text_of_comment",
            "date_added",
        )
