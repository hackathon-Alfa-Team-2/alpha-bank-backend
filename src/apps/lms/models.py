from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint

from src.apps.users.models import CustomUser
from config.settings import (
    DEFAULT_ASSESSMENT_BEFORE,
    DEFAULT_ASSESSMENT_AFTER,
    MAX_SKILLS_ASSESSMENT,
    MIN_SKILLS_ASSESSMENT,
    NAME_FIELD_LENGTH,
    STATUS_FIELD_LENGTH,
)


class Status(models.TextChoices):
    IN_PROGRESS = "В работе", "in_progress"
    NOT_DONE = "Не выполнен", "not_done"
    COMPLETED = "Выполнен", "completed"
    ABSENT = "Отсутствует", "absent"
    CANCELED = "Отменен", "canceled"


class LMS(models.Model):
    """Индивидуальный план развития."""

    name = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        help_text="Введите название ИПР.",
        verbose_name="Название ИПР.",
    )
    description = models.TextField(
        help_text="Введите подробное описание ИПР.",
        verbose_name="Описание ИПР.",
    )
    is_active = models.BooleanField(
        blank=False,
        null=False,
        default=False,
    )
    deadline = models.DateField(
        help_text="Дата дедлайна не может быть раньше текущей.",
        verbose_name="Дата дедлайна.",
    )
    status = models.CharField(
        max_length=STATUS_FIELD_LENGTH,
        verbose_name="Статус ИПР.",
        choices=Status.choices,
        default=Status.ABSENT,
    )
    skill_assessment_before = models.PositiveSmallIntegerField(
        default=DEFAULT_ASSESSMENT_BEFORE,
        verbose_name="Оценка до.",
        validators=[
            MinValueValidator(
                limit_value=MIN_SKILLS_ASSESSMENT,
                message=f"Не может быть меньше {MAX_SKILLS_ASSESSMENT}.",
            ),
            MaxValueValidator(
                limit_value=MAX_SKILLS_ASSESSMENT,
                message=f"Не может быть больше {MAX_SKILLS_ASSESSMENT}.",
            ),
        ],
    )
    skill_assessment_after = models.PositiveSmallIntegerField(
        default=DEFAULT_ASSESSMENT_AFTER,
        verbose_name="Оценка после.",
        validators=[
            MinValueValidator(
                limit_value=MIN_SKILLS_ASSESSMENT,
                message=f"Не может быть меньше {MAX_SKILLS_ASSESSMENT}.",
            ),
            MaxValueValidator(
                limit_value=MAX_SKILLS_ASSESSMENT,
                message=f"Не может быть больше {MAX_SKILLS_ASSESSMENT}.",
            ),
        ],
    )
    date_added = models.DateField(auto_now=True)
    employee = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="employee_lms",
        verbose_name="Сотрудник.",
    )
    supervisor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="supervisor_lms",
        verbose_name="Руководитель.",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ИПР"
        verbose_name_plural = "ИПР"
        constraints = [
            UniqueConstraint(
                fields=["employee", "supervisor"],
                name="unique_employee_supervisor",
            ),
            CheckConstraint(
                check=~Q(
                    is_active=True,
                    employee__employee_lms_is_active=True,
                    # TODO Проверить в постмане
                ),
                name="unique_active_lms_per_employee",
            ),
        ]

    def clean(self):
        # Проверка: нельзя поставить оценку ниже предыдущей.
        if self.skill_assessment_before > self.skill_assessment_after:
            raise ValidationError(
                "Оценка до не может быть больше, чем оценка после."
            )
