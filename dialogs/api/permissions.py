from rest_framework import permissions


class IsInDialog(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        member = None
        try:
            member = obj.membership_set.filter(is_active=True).get(user=request.user)
        except:
            pass
        return bool(member)
