from django.urls import path, include

app_name = "api_v1"

urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include("src.apps.swagger.routes")),
    path("", include("src.apps.users.urls")),
    path("", include("src.apps.lms.urls")),
    path("", include("src.apps.tasks.urls")),
    path("", include("src.apps.comments.urls")),
]
