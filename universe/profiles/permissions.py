from rest_framework import permissions
from .models import Profile

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    This permission only allows owner to edit posts
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwners(permissions.BasePermission):
    """
    This permission only allows owner to View posts
    """

    def has_permission(self, request, view):
        user = request.user
        not_owner = Profile.objects.filter(user= user)
        return not_owner