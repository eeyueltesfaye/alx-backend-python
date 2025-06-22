from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_403_FORBIDDEN
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsAuthenticatedAndParticipant
from .pagination import CustomPagination


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedAndParticipant]
    pagination_class = CustomPagination

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if not conversation_id:
            raise NotFound("conversation_id query parameter is required.")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation does not exist.")

        if self.request.user not in conversation.participants.all():
            return Response({"detail": "You do not have permission to view messages in this conversation."},
                            status=HTTP_403_FORBIDDEN)

        return Message.objects.filter(conversation=conversation).order_by('-timestamp')

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation_id')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation does not exist.")

        if self.request.user not in conversation.participants.all():
            raise Response({"detail": "You do not have permission to send messages in this conversation."},
                           status=HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
