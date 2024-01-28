from datetime import timedelta

from django.utils import timezone


def user_avatar_path(instance, filename):
    return f"avatar/user_{instance.id}/{filename}"


def get_current_month_range():
    today = timezone.now().date()
    month_start = today.replace(day=1)
    next_month = month_start.month + 1
    if next_month > 12:
        next_month -= 12
    next_month_start = month_start.replace(month=next_month)
    month_end = next_month_start - timedelta(days=1)
    return month_start, month_end
