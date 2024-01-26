from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks.views import TaskViewSet

router_v1 = DefaultRouter()
router_v1.register(
    r"users/<user_id>/lms/(?P<lms_id>d+)/task/", TaskViewSet, basename="tasks"
)

urlpatterns = [
    path("", include(router_v1.urls)),
]
