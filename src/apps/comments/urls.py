from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.apps.comments.views import CommentViewSet

comment_router = DefaultRouter()

comment_router.register(
    r"users/lms/tasks/(?P<task_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("", include(comment_router.urls)),
]
