from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from config.settings import NAME_FIELD_LENGTH, STATUS_FIELD_LENGTH
from src.apps.lms.models import LMS, Status


class Task(models.Model):
    """Задача, привязана к ИПР."""

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
        max_length=STATUS_FIELD_LENGTH,
        verbose_name="Статус задачи.",
        choices=Status.choices,
        default=Status.ABSENT,
    )
    date_added = models.DateTimeField(
        auto_now=True,
        editable=False,
    )
    lms = models.ForeignKey(
        LMS,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="ИПР.",
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
