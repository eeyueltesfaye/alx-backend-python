from rest_framework import serializers

from .models import Conversation, Message, User


# from rest_framework.serializers import CharField, SerializerMethodField, ValidationError


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

    def validate_first_name(value):
        if len(value) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long.")
        return value

    def validate_phone_number(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    sent_by = UserSerializer(read_only=True)
    message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'message_body', 'sent_by', 'sent_at', 'message_preview']

    def get_message_preview(self, obj):
        return obj.message_body[:30]

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty or only whitespace.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
