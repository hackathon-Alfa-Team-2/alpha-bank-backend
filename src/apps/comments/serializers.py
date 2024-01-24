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
        attrs["comment_author"] = self.context["request"].user
        attrs["task_id"] = self.context["request"].parser_context["kwargs"][
            "task_id"
        ]
        return attrs
