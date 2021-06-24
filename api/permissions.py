from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin to edit object.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )


class AdminModeratorOrAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if (request.method in ['PATCH', 'DELETE']
                and not request.user.is_anonymous):
            return (
                request.user == obj.author
                or request.user.is_superuser
                or request.user.is_admin()
                or request.user.is_moderator()
            )
        return request.method in permissions.SAFE_METHODS
