from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "Allowed only for owner"

    def has_object_permission(self, request, view, obj):
        return obj.owner.user == request.user


class IsCommenter(permissions.BasePermission):
    message = "Allowed only for owner"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user.profile
