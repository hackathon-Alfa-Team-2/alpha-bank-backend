from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from src.apps.tasks.models import Task


CustomUser = get_user_model()


class Comment(models.Model):
    """Комментарий к задаче."""

    text_of_comment = models.TextField(
        help_text="Добавьте Ваш комментарий.",
        verbose_name="Комментарий.",
        blank=False,
    )
    date_added = models.DateField(
        auto_now=True,
        editable=False,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Задача.",
    )
    comment_author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Сотрудник оставивший комментарий.",
    )

    def __str__(self):
        return f"Комментарий {self.comment_author} {self.date_added}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии."

    def clean(self):
        # Проверка: комментарий может оставить только сотрудник,
        # чья это задача.
        if (
            self.comment_author != self.task.lms.employee
            or self.comment_author != self.task.lms.supervisor
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
