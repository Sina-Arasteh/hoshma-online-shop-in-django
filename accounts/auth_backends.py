from django.contrib.auth.backends import BaseBackend
from .models import CustomUser


class PhoneEmailBackend(BaseBackend):
    def authenticate(self, request, identifier=None, password=None):
        user = CustomUser.objects.get_by_natural_key(identifier)
        if user is not None and user.check_password(password):
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
