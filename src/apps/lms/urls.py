from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.apps.lms.views import LMSStatisticApiView
from src.apps.lms.views import LMSViewSet

lms_router_v1 = DefaultRouter()
lms_router_v1.register(
    r"users/(?P<user_id>\d+)/lms",
    LMSViewSet,
    basename="lms",
)

urlpatterns = [
    path("", include(lms_router_v1.urls)),
    path("lms/statistic/", LMSStatisticApiView.as_view()),
]
