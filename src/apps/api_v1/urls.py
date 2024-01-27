from django.urls import path, include

urlpatterns = [
    path("", include("src.apps.users.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include("src.apps.swagger.routes")),
    path("", include("src.apps.tasks.urls")),
    path("", include("src.apps.comments.urls")),
]
