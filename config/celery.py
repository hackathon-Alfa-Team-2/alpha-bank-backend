import os

from celery import Celery
from environs import Env
from config.settings import STATISTIC_UPDATE_SECONDS

env = Env()
env.read_env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update_stats_cache": {
        "task": "update_stats_cache",
        "schedule": STATISTIC_UPDATE_SECONDS,
    }
}
