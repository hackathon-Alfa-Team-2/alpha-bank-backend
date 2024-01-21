from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from unidecode import unidecode

from config.settings import (
    EMPLOYEE_NAME_LENGTH,
    ROLE_NAME_LENGTH,
    GRADE_NAME_LENGTH,
    POSITION_NAME_LENGTH,
    EMAIL_LENGTH,
    USERNAME_LENGTH,
)
from src.base.utils import user_avatar_path


class Role(models.Model):
    name = models.CharField(max_length=ROLE_NAME_LENGTH)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=GRADE_NAME_LENGTH)

    class Meta:
        verbose_name = "Грейд"
        verbose_name_plural = "Грейды"

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=POSITION_NAME_LENGTH)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=USERNAME_LENGTH,
        unique=True,
        verbose_name="Логин",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        max_length=EMAIL_LENGTH, blank=True, null=True, verbose_name="Email"
    )
    first_name = models.CharField(
        max_length=EMPLOYEE_NAME_LENGTH, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=EMPLOYEE_NAME_LENGTH, verbose_name="Фамилия"
    )
    second_name = models.CharField(
        max_length=EMPLOYEE_NAME_LENGTH,
        verbose_name="Отчество",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
        ],
        verbose_name="Фото",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        verbose_name="Роль",
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        verbose_name="Грейд",
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        verbose_name="Должность",
    )
    supervisor = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="subordinates",
        null=True,
        blank=True,
        verbose_name="Руководитель",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"], name="unique_user"
            ),
            models.UniqueConstraint(fields=["email"], name="unique_email"),
            models.CheckConstraint(
                check=~models.Q(username="me"), name="not_me"
            ),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def generate_username(self):
        username = unidecode(
            f"{self.first_name.lower()}_{self.last_name.lower()}"
        )
        existing_usernames = CustomUser.objects.filter(
            username__startswith=username
        )
        suffix = 1
        while existing_usernames.exists():
            username = f"{username}_{suffix}"
            suffix += 1
            existing_usernames = CustomUser.objects.filter(
                username__startswith=username
            )
        return username

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()
        super(CustomUser, self).save(*args, **kwargs)

    @property
    def is_supervisor(self):
        return self.role.name == "supervisor"
