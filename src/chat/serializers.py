from rest_framework import serializers
from account.serializers import UserSerializer
from .models import ChatAttachment, ChatVideo, ChatVoice, Conversation, ConversationMessage


class ChatAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatAttachment
        fields = ('id', 'get_image',)
        
class ChatVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatVideo
        fields = ('id', 'get_video',)
        
class ChatVoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatVoice
        fields = ('id', 'get_voice',)

class ConversationSerialiser(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    
    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted')
        
class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    attachments = ChatAttachmentSerializer(read_only=True, many=True)
    videos = ChatVideoSerializer(read_only=True, many=True)
    voices = ChatVoiceSerializer(read_only=True, many=True)
    
    class Meta:
        model = ConversationMessage
        fields = ('id', 'body', 'sent_to', 'created_by', 'created_at_formatted', 'attachments', 'videos', 'voices')
        
class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(read_only=True, many=True)
    
    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'messages')