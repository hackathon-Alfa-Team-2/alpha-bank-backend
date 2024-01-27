from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from src.apps.users.filters import CustomUserFilter
from src.apps.users.models import CustomUser
from src.apps.users.paginations import CustomUsersPagination
from src.apps.users.serializers import (
    CustomUserRetrieveSerializer,
    CustomUserListSerializer,
)
from src.base.permissions import IsAdminOrSupervisorReadOnly


class UserReadOnlyModelViewSet(ReadOnlyModelViewSet):
    """Представление пользователей."""

    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrSupervisorReadOnly]
    pagination_class = CustomUsersPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["^first_name", "^last_name", "^position__name"]
    filterset_class = CustomUserFilter

    def get_queryset(self):
        user = self.request.user
        if getattr(self, "swagger_fake_view", False):
            return self.queryset.none()
        if self.action == "me":
            return self.queryset.filter(id=user.id)
        return self.queryset.filter(supervisor=user)

    def get_serializer_class(self):
        if self.action == "list":
            return CustomUserListSerializer
        return CustomUserRetrieveSerializer

    @action(
        url_name="me",
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request: Request):
        user = self.get_queryset().first()
        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
