from rest_framework.serializers import ModelSerializer

from .models import Page
from account.serializers import UserSerializer
from post.serializers import PostSerializer, StorySerializer

class PageSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)
    admins = UserSerializer(read_only=True, many=True)
    subscribers = UserSerializer(read_only=True, many=True)
    posts = PostSerializer(read_only=True, many=True)
    stories = StorySerializer(read_only=True, many=True)
    
    class Meta:
        model = Page
        fields = ('id', 'name', 'description', 'cover', 'subscribers', 'subscribers_count', 'admins', 'posts', 'stories', 'posts_count', 'created_by',)