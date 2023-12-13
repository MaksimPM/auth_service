from rest_framework.permissions import BasePermission


class IsOwnerProfile(BasePermission):
    """Разрешает доступ к профилю только владельцу или персоналу"""

    def has_object_permission(self, request, view, obj):
        if request.user == obj or request.user.is_staff:
            return True
        return False
