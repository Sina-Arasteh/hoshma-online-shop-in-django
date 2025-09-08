from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class MaximumLengthValidator:
    def __init__(self, max_length=128):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _(f"This password must contain at least {self.max_length} characters."),
                code="password_too_long"
            )
    
    def get_help_text(self):
        return _(f"You password must contain at least {self.max_length} characters.")
