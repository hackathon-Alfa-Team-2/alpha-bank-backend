from django.urls import path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Индивидуальный план развития API",
        default_version="v1",
        description="Документация для проекта Индивидуальный план развития",
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
    url=settings.BASE_REQUEST_URL,
)

urlpatterns = [
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", RedirectView.as_view(url="docs/", permanent=False), name="index"),
]
