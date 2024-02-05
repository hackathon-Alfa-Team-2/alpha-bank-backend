from django.contrib import admin

from src.apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_added",
        "comment_author",
        "flagged",
    )
    list_display_links = ("id",)
    list_editable = ("flagged",)
    search_fields = "comment_author__last_name", "employee__name"
    search_help_text = "Поиск по Фамилии автора."
