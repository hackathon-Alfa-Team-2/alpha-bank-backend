from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.apps.lms.models import LMS
from src.apps.lms.serializers import FullDataLMSSerializer
from src.base.permissions import IsAdminOrSupervisorOrLMSExecutor


class LMSViewSet(viewsets.ModelViewSet):
    serializer_class = FullDataLMSSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSupervisorOrLMSExecutor]

    def perform_create(self, serializer):
        supervisor = self.request.user
        serializer.save(supervisor=supervisor)

    def get_queryset(self):
        user = self.request.user
        url_user = self.kwargs.get("user_id")
        if user.is_supervisor:
            return LMS.objects.select_related("supervisor").filter(
                supervisor=user, employee_id=url_user
            )
        if user.role.name == "employee":
            return LMS.objects.select_related("employee").filter(employee=user)
        return LMS.objects.all()
