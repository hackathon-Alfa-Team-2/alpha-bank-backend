from celery import shared_task
from django.core.cache import cache
from django.db.models import Count, Case, When

from src.apps.lms.models import LMS
from src.base.utils import get_current_month_range


@shared_task(name="update_stats_cache")
def update_stats_cache():
    month_start, month_end = get_current_month_range()
    stats_data = LMS.objects.aggregate(
        total_count=Count("id"),
        deadlines_this_month=Count(
            Case(
                When(
                    deadline__gte=month_start,
                    deadline__lte=month_end,
                    then=1,
                )
            )
        ),
        completed_count=Count(Case(When(status="completed", then=1))),
    )
    cache.set("stats", stats_data, timeout=None)
    return stats_data
