from rest_framework import permissions


class IsUserOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the account.
        return obj == request.user or request.user.is_superuser


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the account.
        return obj.user == request.user or request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superuser to edit it.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # Write permissions are only allowed to the owner of the snippet.
            return request.user.is_superuser


class IsStaff(permissions.BasePermission):
    """
    Custom permission to only allow superuser to edit it.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # Write permissions are only allowed to the owner of the snippet.
            return request.user.is_staff


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superuser to edit it.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
