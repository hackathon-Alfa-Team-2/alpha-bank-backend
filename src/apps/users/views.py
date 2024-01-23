from django.contrib.auth import get_user_model
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from src.apps.users.serializers import (
    CustomUserRetrieveSerializer,
    CustomUserListSerializer,
)
from src.base.permissions import IsAdminOrSupervisorReadOnly

CustomUser = get_user_model()


class UserReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrSupervisorReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "position__name"]

    # TODO фильтрация по статусу и дедлайну

    def get_queryset(self):
        user = self.request.user
        if self.action in ["retrieve", "list"]:
            return CustomUser.objects.filter(supervisor=user)
        if self.action == "me":
            return CustomUser.objects.filter(id=user.id)

    def get_serializer_class(self):
        if self.action in ["retrieve", "me"]:
            return CustomUserRetrieveSerializer
        if self.action == "list":
            return CustomUserListSerializer

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
