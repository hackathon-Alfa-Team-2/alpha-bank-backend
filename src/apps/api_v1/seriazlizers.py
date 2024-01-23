from datetime import date
from rest_framework import serializers

from tasks.models import Task
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    second_name = serializers.CharField(max_length=150)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "second_name",
        )


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TaskReadSerializer(DynamicFieldsModelSerializer):
    name = serializers.CharField(source="title")
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ("id", "name", "author", "description", "comments")

    def get_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user

    def validate_deadline(self, value):
        """
        Проверяем, что дедлайн не раньше текущей даты.
        """
        if value <= (
            self.instance.date_added if self.instance else date.today()
        ):
            raise serializers.ValidationError(
                "Дедлайн не может быть раньше или равен текущей дате."
            )
        return value
