from django.contrib.auth import get_user_model
from rest_framework import serializers

from src.apps.lms.models import LMS
from src.apps.lms.serializers import ShortDataLMSSerializer

CustomUser = get_user_model()


class CustomUserListSerializer(serializers.ModelSerializer):
    """
    Серилизатор списка пользователей с активным ИПР если такой существует.
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
            "photo",
            "active_lms",
        )
        read_only_fields = ("__all__",)

    def get_active_lms(self, employee):
        active_lms = LMS.objects.filter(
            employee=employee, is_active=True
        ).first()
        return ShortDataLMSSerializer(active_lms).data


class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя со всеми принадлежащими ему ИПР.
    """

    position = serializers.StringRelatedField()
    grade = serializers.StringRelatedField()
    role = serializers.StringRelatedField()
    lms = ShortDataLMSSerializer(
        many=True,
        source="employee_lms",
    )

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
            "lms",
        )
        read_only_fields = ("__all__",)
