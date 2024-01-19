import time

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class F(models):
    pass


class CUser(AbstractUser):
    try:
        pass
    except ValidationError:
        pass
    ...


time = time.time()
