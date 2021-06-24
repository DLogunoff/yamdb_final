from rest_framework import permissions


class UserObjectPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'create']:
            rv = request.user.is_authenticated and request.user.is_admin()
            return rv
        else:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if (request.method in ['GET', 'PATCH']
                and obj.username == request.user.username):
            return True
        else:
            return request.user.is_admin()
