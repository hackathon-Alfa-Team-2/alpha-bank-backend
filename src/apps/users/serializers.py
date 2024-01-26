from django.contrib.auth import get_user_model
from rest_framework import serializers

CustomUser = get_user_model()


class CustomUserListSerializer(serializers.ModelSerializer):
    """
    Серилизатор списка пользователей с активным ИПР если такой существует.
    """

    # TODO Добавить active_lms поле SerializerMethodField().

    position = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "second_name",
            "last_name",
            "position",
            "photo",
        )
        read_only_fields = ("__all__",)


class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя со всеми принадлежащими ему ИПР.
    """

    position = serializers.StringRelatedField()
    grade = serializers.StringRelatedField()
    role = serializers.StringRelatedField()

    # TODO Добавить поле lms ShortDataLMSSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "second_name",
            "last_name",
            "position",
            "grade",
            "role",
            "photo",
        )
        read_only_fields = ("__all__",)
