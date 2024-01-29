from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from src.apps.tasks.models import Task
from config.settings import TEXT_FIELD_LENGTH


CustomUser = get_user_model()


class Comment(models.Model):
    """Комментарий к задаче."""

    text_of_comment = models.TextField(
        max_length=TEXT_FIELD_LENGTH,
        help_text="Добавьте Ваш комментарий",
        verbose_name="Комментарий",
        blank=False,
    )
    date_added = models.DateTimeField(
        auto_now=True,
        editable=False,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Задача",
    )
    comment_author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Сотрудник оставивший комментарий",
    )
    flagged = models.BooleanField(default=False)

    def __str__(self):
        return f"Комментарий {self.comment_author} {self.date_added}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def save(self, *args, **kwargs):
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
        else:
            super().save(*args, **kwargs)
