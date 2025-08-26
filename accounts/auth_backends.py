from django.contrib.auth.backends import BaseBackend
from .models import CustomUser


class PhoneEmailBackend(BaseBackend):
    def authenticate(self, request, identifier=None, password=None):
        try:
            user = CustomUser.objects.get_by_natural_key(identifier)
            if user.check_password(password):
                return user
            return None
        except CustomUser.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
