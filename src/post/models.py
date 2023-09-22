from django.db import models
from datetime import datetime, timezone
from django.utils.timesince import timesince
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from account.models import User


class Like(models.Model):
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)

class PostAttachment(models.Model):
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return ''
        
def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 10MB limit
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    
class PostVideo(models.Model):
    video = models.FileField(upload_to='post_videos', 
                             validators=[
                                validate_file_size
                            ])
    created_by = models.ForeignKey(User, related_name='post_videos', on_delete=models.CASCADE)
    
    def get_video(self):
        if self.video:
            return self.video.url
        else:
            return ''
        
        
class Post(models.Model):
    body = models.TextField(blank=True, null=True)
    
    attachments = models.ManyToManyField(PostAttachment, blank=True)
    
    videos = models.ManyToManyField(PostVideo, blank=True)

    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)

    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts_user', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)
   
class Story(models.Model):
    body = models.TextField(blank=True, null=True)
    
    attachments = models.ManyToManyField(PostAttachment, blank=True)
    
    videos = models.ManyToManyField(PostVideo, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='stories_user', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
        time_difference = datetime.now(timezone.utc) - self.created_at
        seconds = int(time_difference.total_seconds())
        hours = seconds // 3600
        minutes = (seconds // 60) % 60

        if seconds >= 86400:  # 24 hours in seconds
            self.delete()

        if hours >= 1:
            return f"{hours} hours"
        else:
            return f"{minutes} minutes"
   
#    def created_at_formatted(self):
#         time_difference = timezone.now() - self.created_at
        
#         hours = time_difference.seconds // 3600
#         minutes = (time_difference.seconds // 60) % 60
        
#         if time_difference.total_seconds() >= 86400:  # 24 hours in seconds
#             self.is_expired = True
#             self.save()
            
#         if hours >= 1:
#             return f"{hours} hours"
#         else:
#             return f"{minutes} minutes"

   
class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()
