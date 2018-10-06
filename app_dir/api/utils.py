from structlog import get_logger
from rest_framework import permissions

logger = get_logger(__name__)


class IsAdminOrPermitted(permissions.BasePermission):
    @staticmethod
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser or user.has_perm(
            "can_create_view_via_API"
        )


class IsPermittedCreateView(permissions.BasePermission):
    @staticmethod
    def has_permission(self, request, view):
        user = request.user
        return user.has_perm(
            "can_create_view_via_API"
        )
