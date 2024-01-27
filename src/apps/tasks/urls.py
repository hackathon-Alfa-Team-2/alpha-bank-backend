from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.apps.tasks.views import TaskViewSet

tasks_router_v1 = DefaultRouter()
tasks_router_v1.register(
    r"users/(?P<user_id>\d+)/lms/(?P<lms_id>\d+)/tasks",
    TaskViewSet,
    basename="tasks",
)

urlpatterns = [
    path("", include(tasks_router_v1.urls)),
]
