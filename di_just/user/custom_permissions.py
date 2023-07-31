from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    message = "Allowed only for owner"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsSameUser(permissions.BasePermission):
    message = "Only allowed for the owner of account"

    def has_object_permission(self, request, view, obj):
        return obj == request.user
