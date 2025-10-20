from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_not_in_past(value):
    if value < timezone.now():    # timezone implies only date or both date and time????
        raise ValidationError(
            _("You cannot enter a past date and time."),
            code='past_date'
        )
