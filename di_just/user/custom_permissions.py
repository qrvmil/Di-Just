from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    message = "Allowed only for owner"

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
