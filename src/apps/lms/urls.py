from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.apps.lms.views import LMSViewSet

lms_router_v1 = DefaultRouter()
lms_router_v1.register("lms", LMSViewSet)

urlpatterns = [
    path("", include(lms_router_v1.urls)),
]
