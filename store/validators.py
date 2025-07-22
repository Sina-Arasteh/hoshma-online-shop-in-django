from django.core.exceptions import ValidationError
from django.utils import timezone


def not_in_past_validator(value):
    if value < timezone.now():
        raise ValidationError("تاریخ و زمان شروع تخفیف نمی‌تواند در گذشته باشد.")
