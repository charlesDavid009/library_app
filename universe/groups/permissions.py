from rest_framework import permissions
from .models import Group


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    This permission only allows owner to edit posts
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwners(permissions.BasePermission):
    """
    This permission only allows owner to View posts
    """

    def has_permission(self, request, view):
        user = request.user
        not_owner = Group.objects.filter(owner= user)
        return not not_owner

class IsFollower(permissions.BasePermission):
    """
    This permissions only allows users to view
    """

    def has_permission(self, request, view):
        user = request.user
        is_follower= Group.objects.filter(follower = user).exists()
        return is_follower

class IsUsers(permissions.BasePermission):
    """
    This permissions only allows users to view
    """

    def has_permission(self, request, view):
        user = request.user
        is_user= Group.objects.filter(users = user).exists()
        return is_user


class MyAdmin(permissions.BasePermission):
    """
    This permission admin to perform actions
    """

    def has_permission(self, request, view):
        user = request.user
        is_admin = Group.objects.filter(admin=user).exists()
        return  is_admin

