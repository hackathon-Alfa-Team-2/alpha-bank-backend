from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.settings import CACHE_MIDDLEWARE_SECONDS
from src.apps.lms.models import LMS
from src.apps.lms.serializers import FullDataLMSSerializer, StatisticSerializer
from src.base.permissions import IsAdminOrSupervisorOrLMSExecutor
from src.base.tasks import update_stats_cache


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

    @method_decorator(cache_page(CACHE_MIDDLEWARE_SECONDS))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_MIDDLEWARE_SECONDS))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class LMSStatisticApiView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StatisticSerializer
    swagger_tags = ["LMS"]

    @method_decorator(cache_page(CACHE_MIDDLEWARE_SECONDS))
    def get(self, request, *args, **kwargs):
        stats_data = cache.get("stats")
        if not stats_data:
            update_stats_cache()
            stats_data = cache.get("stats")
        serializer = self.serializer_class(data=stats_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
