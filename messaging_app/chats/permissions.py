from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to view/edit their own conversations or messages.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated first
        if not request.user or not request.user.is_authenticated:
            return False

        # Then check ownership
        return obj.user == request.user or (
            hasattr(obj, 'conversation') and obj.conversation.user == request.user
        )
