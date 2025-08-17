from rest_framework import permissions
from django.utils.translation import gettext_lazy as _

class IsAdminOrReadOnly(permissions.BasePermission):
    message = _("You must be an admin to modify this resource.")

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return False
