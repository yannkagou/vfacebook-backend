from django.db import models
from django.utils.timesince import timesince

from account.models import User
from post.models import Post, Story

class Page(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    cover = models.ImageField(upload_to='covers', null=True, blank=True)
    
    subscribers = models.ManyToManyField(User, related_name='followed_pages')
    subscribers_count = models.IntegerField(default=0)
    admins = models.ManyToManyField(User, related_name='admin_pages')
    
    posts = models.ManyToManyField(Post, blank=True)
    stories = models.ManyToManyField(Story, blank=True)
    posts_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='pages', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)
