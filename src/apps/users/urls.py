from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.apps.users.views import UserReadOnlyModelViewSet

users_router_v1 = DefaultRouter()
users_router_v1.register(
    "users",
    UserReadOnlyModelViewSet,
    basename="users",
)

urlpatterns = [
    path("", include(users_router_v1.urls)),
]
