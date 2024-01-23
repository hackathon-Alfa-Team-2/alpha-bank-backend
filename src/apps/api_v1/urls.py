from django.urls import path, include

urlpatterns = [
    path("", include("src.apps.users.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
