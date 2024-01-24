from rest_framework.routers import DefaultRouter
from django.urls import path, include

from src.apps.comments.views import CommentViewSet

comment_router = DefaultRouter()

comment_router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("lms/tasks/<int:pk>/", include(comment_router.urls)),
]
