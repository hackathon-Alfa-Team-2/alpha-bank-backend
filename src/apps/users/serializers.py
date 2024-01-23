from django.contrib.auth import get_user_model
from rest_framework import serializers

from src.apps.lms.models import LMS

CustomUser = get_user_model()


class CustomUserListSerializer(serializers.ModelSerializer):
    """
    Вывод списка пользователей с активным ИПР если такой существует.
    """

    active_lms = serializers.SerializerMethodField()
    position = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "second_name",
            "last_name",
            "position",
            "active_lms",
            "photo",
        )
        read_only_fields = ("__all__",)

    def get_active_lms(self, obj: CustomUser):
        """
        Получить активный ИПР пользователя.
        """
        return LMS.objects.filter(employee=obj, is_active=True).first()


class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    """
    Вывод пользователя со всеми принадлежащими ему ИПР.
    """

    position = serializers.StringRelatedField()
    grade = serializers.StringRelatedField()
    role = serializers.StringRelatedField()

    # lms = ...  # ShortDataLMSSerializer(many=True)

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
            # "lms",
        )
        read_only_fields = ("__all__",)
