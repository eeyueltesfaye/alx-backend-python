from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to view/edit their own conversations or messages.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or getattr(obj, 'conversation', None) and obj.conversation.user == request.user
