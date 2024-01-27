from django.db.models import Q
from django_filters.rest_framework import FilterSet, filters

from src.apps.users.models import CustomUser


class CustomUserFilter(FilterSet):
    """
    Кастомный фильтр для представления пользователей.
    Фильтрация по статусу активного ИПР.
    Фильтрация по диапазону дедлайна.
    """

    status = filters.CharFilter(
        field_name="employee_lms__status", method="get_status"
    )
    deadline = filters.DateFromToRangeFilter(
        field_name="employee_lms__deadline", method="get_deadline_range"
    )

    def get_status(self, queryset, name, value):
        return queryset.filter(
            employee_lms__status=value, employee_lms__is_active=True
        )

    def get_deadline_range(self, queryset, name, value):
        if not value.start or not value.stop:
            return queryset
        return queryset.filter(
            Q(
                employee_lms__deadline__gte=value.start,
                employee_lms__is_active=True,
            )
            & Q(
                employee_lms__deadline__lte=value.stop,
                employee_lms__is_active=True,
            ),
        )

    class Meta:
        model = CustomUser
        fields = ["employee_lms"]
