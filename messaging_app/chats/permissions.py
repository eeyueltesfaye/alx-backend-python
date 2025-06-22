from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to view/edit their own content,
    including support for PUT, PATCH, and DELETE methods.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated for any method
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Additional ownership check per object, especially for safe vs. unsafe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user or (
            hasattr(obj, 'conversation') and obj.conversation.user == request.user
        )
