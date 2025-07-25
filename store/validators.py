from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def not_in_past_validator(value):
    if value < timezone.now():
        raise ValidationError(_("You cannot enter a past date and time."))
