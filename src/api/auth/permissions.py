from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperUser(permissions.BasePermission):
    """The user is a superuser."""

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """The user is a superuser or readonly."""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )


class IsStaff(permissions.BasePermission):
    """The user is staff."""

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_staff
        )


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user and request.user.is_authenticated and request.user.is_administrator
        )
