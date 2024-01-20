from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from src.apps.tasks.models import Task

User = get_user_model()


class Comment(models.Model):
    """Комментарий к задаче."""

    text_of_comment = models.TextField(
        help_text="Добавьте Ваш комментарий.",
        verbose_name="Комментарий.",
    )
    date_added = models.DateField(
        auto_now=True,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Комментарий к задаче.",
    )
    comment_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_author",
        verbose_name="Сотрудник оставивший комментарий.",
    )

    def __str__(self):
        return f"Комментарий {self.comment_author} {self.date_added}"

    def clean(self):
        # Проверка: комментарий может оставить только сотрудник,
        # чья это задача.
        if (
            self.comment_author != self.task.lms.employee
            and self.comment_author != self.task.lms.supervisor
        ):
            raise ValidationError(
                "Комментарий может оставить только сотрудник или"
                " его руководитель."
            )

        # Проверка: руководитель может оставлять комментарии
        # только к своим задачам.
        if (
            self.comment_author == self.task.lms.supervisor
            and self.comment_author != self.task.lms.employee
        ):
            raise ValidationError(
                "Руководитель может оставлять комментарии только"
                " к своим задачам."
            )
