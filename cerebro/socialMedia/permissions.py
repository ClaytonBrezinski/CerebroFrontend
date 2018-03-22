from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Admin user class, will allow anyone GET, HEAD, and OPTIONS to non-admins.
    Will allow admins to do PUT, UPDATE, and DELETE posts
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff