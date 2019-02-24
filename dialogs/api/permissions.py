from rest_framework import permissions


class IsInDialog(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        members = obj.members.all()
        user = request.user
        return user in members
