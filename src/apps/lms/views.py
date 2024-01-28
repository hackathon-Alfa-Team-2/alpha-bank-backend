from django.db.models import Count, Case, When
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.apps.lms.models import LMS
from src.apps.lms.serializers import FullDataLMSSerializer, StatisticSerializer
from src.base.permissions import IsAdminOrSupervisorOrLMSExecutor
from src.base.utils import get_current_month_range


class LMSViewSet(viewsets.ModelViewSet):
    serializer_class = FullDataLMSSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSupervisorOrLMSExecutor]
    swagger_tags = ["LMS"]

    def get_queryset(self):
        user = self.request.user
        if getattr(self, "swagger_fake_view", False):
            return LMS.objects.none()
        if user.is_supervisor:
            return LMS.objects.select_related("supervisor").filter(
                supervisor=user,
                employee_id=self.kwargs.get("user_id"),
            )
        if user.role.name == "employee":
            return LMS.objects.select_related("employee").filter(
                employee=user,
            )
        return LMS.objects.all()

    @action(
        url_name="statistic",
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def statistic(self, request, *args, **kwargs):
        month_start, month_end = get_current_month_range()
        stats_data = LMS.objects.aggregate(
            total_count=Count("id"),
            deadlines_this_month=Count(
                Case(
                    When(
                        deadline__gte=month_start,
                        deadline__lte=month_end,
                        then=1,
                    )
                )
            ),
            completed_count=Count(Case(When(status="completed", then=1))),
        )
        serializer = StatisticSerializer(data=stats_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
