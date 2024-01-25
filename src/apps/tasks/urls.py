from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks.views import TaskViewSet

app_name = "tasks"

router_v1 = DefaultRouter()
router_v1.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("", include(router_v1.urls)),
]
