from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Like, Post, PostAttachment, PostVideo, Comment, Trend, Story

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image',)
        
class PostVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideo
        fields = ('id', 'get_video',)

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted',)
        
class LikeSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'created_by', 'created_at',)
        
class StorySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    videos = PostVideoSerializer(read_only=True, many=True)

    class Meta:
        model = Story
        fields = ('id', 'body', 'created_by', 'created_at_formatted', 'attachments', 'videos',)
        
class StoryDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    videos = PostVideoSerializer(read_only=True, many=True)

    class Meta:
        model = Story
        fields = ('id', 'body', 'created_by', 'created_at_formatted', 'attachments', 'videos',)
        
class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    videos = PostVideoSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes', 'likes_count', 'comments_count', 'created_by', 'created_at_formatted','comments', 'attachments', 'videos',)


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    videos = PostVideoSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'comments_count', 'created_by', 'created_at_formatted', 'comments', 'attachments', 'videos',)
        
class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trend
        fields = ('id', 'hashtag', 'occurences',)