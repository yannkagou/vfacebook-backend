from django.http import JsonResponse
from rest_framework.decorators import api_view

from .forms import MessageForm
from .models import ChatAttachment, ChatVideo, ChatVoice, Conversation, ConversationMessage
from .serializers import ConversationSerialiser, ConversationMessageSerializer, ConversationDetailSerializer
from account.models import User

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    serializer = ConversationSerialiser(conversations, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_detail(request, id):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(id=id)
    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_get_or_create(request, user_id):
    user = User.objects.get(id=user_id)
    
    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))
    
    if conversations.exists():
        conversation = conversations.first()
        print("Conversation exists")   
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()
        print("Conversation created") 
    serializer = ConversationDetailSerializer(conversation)
        
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def conversation_send_message(request, id):
    conversation = Conversation.objects.filter(users__in=[request.user]).get(id=id)
    sent_to = None

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user
            break

    form = MessageForm(request.POST)
    if form.is_valid():
        conversation_message = form.save(commit=False)
        conversation_message.conversation = conversation
        conversation_message.created_by = request.user
        conversation_message.sent_to = sent_to
        conversation_message.save()

        attachments = request.FILES.getlist('image')
        videos = request.FILES.getlist('video')
        voices = request.FILES.getlist('voice')

        for attachment in attachments:
            attachment_instance = ChatAttachment.objects.create(image=attachment, created_by=request.user)
            conversation_message.attachments.add(attachment_instance)

        for video in videos:
            video_instance = ChatVideo.objects.create(video=video, created_by=request.user)
            conversation_message.videos.add(video_instance)

        for voice in voices:
            voice_instance = ChatVoice.objects.create(voice=voice, created_by=request.user)
            conversation_message.voices.add(voice_instance)

        serializer = ConversationMessageSerializer(conversation_message)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid form data for chat'})
    