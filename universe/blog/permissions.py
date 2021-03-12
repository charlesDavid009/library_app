from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    This permission only allows owner to edit posts
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsOwner(permissions.BasePermission):
    """
    This permission only allows owner to View posts
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
