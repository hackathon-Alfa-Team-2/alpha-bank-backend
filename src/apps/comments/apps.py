from django.apps import AppConfig


class CommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.comments"
    verbose_name = "Комментарии"
