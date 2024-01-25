from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from src.apps.comments.models import Comment


class CommentSerializer(ModelSerializer):
    """Сериализатор комментариев."""

    comment_author = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "comment_author",
            "task_id",
            "text_of_comment",
            "flagged",
            "date_added",
        )

    def validate(self, attrs):
        task_id = self.context["request"].parser_context["kwargs"]["task_id"]
        comment_author = self.context["request"].user
        attrs["comment_author"] = comment_author
        attrs["task_id"] = task_id
        return attrs
