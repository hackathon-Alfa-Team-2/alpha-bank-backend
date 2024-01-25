from rest_framework.pagination import LimitOffsetPagination


class CustomUsersPagination(LimitOffsetPagination):
    default_limit = 5
