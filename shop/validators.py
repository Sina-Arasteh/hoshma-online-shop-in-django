from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_not_in_past(value):
    if value < timezone.now():
        raise ValidationError(
            _("You cannot enter a past date and time."),
            code='invalid_past_date'
        )


def validate_positive_value(value):
    if value <= 0:
        raise ValidationError(
            _("Zero or negative values are not allowed."),
            code='invalid_positive_value'
        )