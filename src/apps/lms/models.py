from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class LMS(models.Model):
    """Индивидуальный план развития."""

    name = models.CharField()
