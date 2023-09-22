from django.db import models
from django.forms import ValidationError
from django.utils.timesince import timesince
from account.models import User


class ChatAttachment(models.Model):
    image = models.ImageField(upload_to='chat_attachments')
    created_by = models.ForeignKey(User, related_name='chat_attachments', on_delete=models.CASCADE)

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return ''
        
def validate_file_size(value):
    filesize = value.size
    if filesize > 3 * 1024 * 1024:  # 10MB limit
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    
class ChatVideo(models.Model):
    video = models.FileField(upload_to='chat_videos', 
                             validators=[
                                validate_file_size
                            ])
    created_by = models.ForeignKey(User, related_name='chat_videos', on_delete=models.CASCADE)
    
    def get_video(self):
        if self.video:
            return self.video.url
        else:
            return ''
        
class ChatVoice(models.Model):
    voice = models.FileField(upload_to='voice_notes/')
    created_by = models.ForeignKey(User, related_name='chat_voices', on_delete=models.CASCADE)

    def get_voice(self):
        if self.voice:
            return self.voice.url
        else:
            return ''


class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def modified_at_formatted(self):
       return timesince(self.modified_at)
    
class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    attachments = models.ManyToManyField(ChatAttachment, blank=True)
    videos = models.ManyToManyField(ChatVideo, blank=True)
    voices = models.ManyToManyField(ChatVoice, blank=True)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def created_at_formatted(self):
       return timesince(self.created_at)
