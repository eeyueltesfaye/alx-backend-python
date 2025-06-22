from rest_framework import serializers
from .models import User, Conversation, Message
from rest_framework import serializers
from .models import Book

class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()
    
    class Meta:
        model = Message
        fields = ['message_id', 'message_body', 'sent_at', 'sender']

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)  # Or use UserSerializer if defined
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
<<<<<<< HEAD
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        messages = obj.message_set.all()
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        # Example validation with ValidationError
        if not data.get('participants'):
            raise serializers.ValidationError("Conversation must have at least one participant.")
        return data
=======
        fields = ['id', 'participants', 'messages', 'created_at']
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
>>>>>>> 9495c56 (Update messaging_app with filters and views)
