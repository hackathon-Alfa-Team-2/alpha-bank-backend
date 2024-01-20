from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint

from config.settings import (
    DEFAULT_ASSESSMENT,
    MAX_SKILLS_ASSESSMENT,
    MIN_SKILLS_ASSESSMENT,
    NAME_FIELD_LENGTH,
)

User = get_user_model()


class LMS(models.Model):
    """Индивидуальный план развития."""

    class LMSStatus(models.TextChoices):
        IN_PROGRESS = "В работе", "in_process"
        NOT_DONE = "Не выполнен", "not_done"
        COMPLETED = "Выполнен", "completed"
        ABSENT = "Отсутствует", "absent"
        CANCELED = "Отменен", "canceled"

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
        verbose_name="Статус ИПР.",
        choices=LMSStatus.choices,
        default=LMSStatus.ABSENT,
    )
    skill_assessment_before = models.PositiveSmallIntegerField(
        default=DEFAULT_ASSESSMENT,
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
        default=DEFAULT_ASSESSMENT,
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
        User,
        on_delete=models.CASCADE,
        related_name="employee_lms",
        verbose_name="Сотрудник, которому назначен ИПР.",
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="supervisor_lms",
        verbose_name="Руководитель, назначивший ИПР.",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ИПР"
        verbose_name_plural = "ИПРы"
        constraints = [
            UniqueConstraint(
                fields=["employee", "supervisor"],
                name="unique_employee_supervisor",
            ),
            CheckConstraint(
                check=~Q(
                    is_active=True, employee__employee_lms__is_active=True
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
