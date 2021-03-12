from rest_framework import permissions
from .models import Page


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    This permission only allows owner to edit posts
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.users == request.user


class IsOwner(permissions.BasePermission):
    """
    This permission only allows owner to View posts
    """

    def has_permission(self, request, view):
        user = request.user
        is_owner = Page.objects.filter(users =user).exists()
        return is_owner
