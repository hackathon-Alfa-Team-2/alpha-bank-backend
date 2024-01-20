from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from config.settings import NAME_FIELD_LENGTH
from src.apps.lms.models import LMS


class Task(models.Model):
    """Задача, привязана к ИПР."""

    class TaskStatus(models.TextChoices):
        IN_PROGRESS = "В работе", "in_process"
        NOT_DONE = "Не выполнена", "not_done"
        COMPLETED = "Выполнена", "completed"
        ABSENT = "Отсутствует", "absent"
        CANCELED = "Отменена", "canceled"

    name = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        help_text="Введите название задачи.",
        verbose_name="Название Задачи.",
    )
    description = models.TextField(
        help_text="Введите подробное описание задачи.",
        verbose_name="Описание.",
    )
    deadline = models.DateField(
        help_text="Дата дедлайна не может быть раньше текущей.",
        verbose_name="Дата дедлайна.",
    )
    status = models.CharField(
        verbose_name="Статус задачи.",
        choices=TaskStatus.choices,
        default=TaskStatus.ABSENT,
    )
    date_added = models.DateField(
        auto_now=True,
    )
    lms = models.ForeignKey(
        LMS,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Задача для развития",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        constraints = [
            UniqueConstraint(fields=["name", "lms"], name="unique_name_lms"),
        ]

    def clean(self):
        # Проверка: дата дэдлайна не может быть раньше даты создания.
        if self.deadline and self.deadline <= self.date_added:
            raise ValidationError(
                "Дедлайн не может быть раньше или равен дате создания."
            )
