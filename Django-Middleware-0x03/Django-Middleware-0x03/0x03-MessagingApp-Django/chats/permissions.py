from rest_framework import permissions

class IsAuthenticatedAndParticipant(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read and write only if the user is a participant
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user in obj.participants.all()
        return False