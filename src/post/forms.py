from django.forms import ModelForm

from .models import Post, Story, PostAttachment, PostVideo


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
        
# class AttachmentForm(ModelForm):
#     class Meta:
#         model = PostAttachment
#         fields = ('image',)
        
# class VideoForm(ModelForm):
#     class Meta:
#         model = PostVideo
#         fields = ('video',)

class StoryForm(ModelForm):
    class Meta:
        model = Story
        fields = ('body',)