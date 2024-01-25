from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from src.apps.comments.models import Comment
from src.apps.tasks.models import Task


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
        task = Task.objects.select_related("lms").filter(
            Q(id=task_id, lms__supervisor=comment_author)
            | Q(id=task_id, lms__employee=comment_author)
        )
        if not task:
            raise serializers.ValidationError(
                detail="You are not allowed to leave a comment on a "
                "task that you are not related to."
            )
        attrs["comment_author"] = comment_author
        attrs["task_id"] = task_id
        return attrs
