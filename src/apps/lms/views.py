from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.apps.lms.models import LMS
from src.apps.lms.serializers import FullDataLMSSerializer
from src.base.permissions import IsAdminOrSupervisorOrLMSExecutor


class LMSViewSet(viewsets.ModelViewSet):
    queryset = LMS.objects.all()
    serializer_class = FullDataLMSSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSupervisorOrLMSExecutor]

    def perform_create(self, serializer):
        supervisor = self.request.user
        serializer.save(supervisor=supervisor)
