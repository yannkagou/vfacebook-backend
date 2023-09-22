from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view

from account.models import User
from account.serializers import UserSerializer
from post.forms import PostForm, StoryForm

from post.models import Comment, Like, Post, PostAttachment, PostVideo
from post.serializers import CommentSerializer, PostSerializer, StorySerializer

# from notification.utils import create_notification

from .models import Page
from .serializers import PageSerializer
from .forms import PageForm

@api_view(['GET'])
def page_list(request):
    pages = Page.objects.all()
    
    serializer = PageSerializer(pages, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def page_detail(request, page_id):
    page = Page.objects.get(id=page_id)
    
    serializer = PageSerializer(page)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['DELETE'])
def page_delete(request, page_id):
    page = Page.objects.get(id=page_id)
    page.delete()
    
    return JsonResponse({'message': 'Page deleted'})

@api_view(['GET'])
def page_list_profile(request, id):   
    user = User.objects.get(id=id)
    pages = Page.objects.filter(Q(subscribers=user) | Q(created_by=user) | Q(admins=user))
    pages_serializer = PageSerializer(pages, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'pages': pages_serializer.data,
        'user': user_serializer.data,
    }, safe=False)
    
@api_view(['POST'])
def page_create(request):
    form = PageForm(request.POST, request.FILES)
    if form.is_valid():
        page = form.save(commit=False)
        page.created_by = request.user
        page.save()
        
        page.subscribers.add(request.user)
        page.admins.add(request.user)
        page.subscribers_count = page.subscribers_count + 1
        page.save()
        
        serializer = PageSerializer(page)
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid form data for page'})
    
@api_view(['POST'])
def subscribe_page(request, page_id):
    page = Page.objects.get(id=page_id)
    
    if request.user in page.subscribers.all():
        page.subscribers.remove(request.user)
        page.subscribers_count = page.subscribers_count - 1
        page.save()
        return JsonResponse({'message': 'page like deleted'})
    else:
        page.subscribers.add(request.user)
        page.subscribers_count = page.subscribers_count + 1
        page.save()
        
        # notification = create_notification(request, 'page_liked', page_id=page.id)

        return JsonResponse({'message': 'Page like created'})
    
    
@api_view(['POST'])
def page_add_admins(request, page_id, id):
    page = Page.objects.get(id=page_id)
    user = User.objects.get(id=id)
    
    if user in page.subscribers.all():
        if user not in page.admins.all():
            page.admins.add(user)
            page.save()
            # notification = create_notification(request, 'page_admin', page_id=page.id)
            return JsonResponse({'message': 'Page admin added'})
        else:
            page.admins.remove(user)
            page.save()
            return JsonResponse({'message': 'Page admin deleted'})
    
@api_view(['POST'])
def page_post_create(request, page_id):
    form = PostForm(request.POST)
    page = Page.objects.get(id=page_id)
    if form.is_valid():
        post = form.save(commit=False)
        post.related_to = page
        post.save()

        attachments = request.FILES.getlist('image')
        videos = request.FILES.getlist('video')

        for attachment in attachments:
            attachment_instance = PostAttachment.objects.create(image=attachment, created_by=request.user)
            post.attachments.add(attachment_instance)

        for video in videos:
            video_instance = PostVideo.objects.create(video=video, created_by=request.user)
            post.videos.add(video_instance)
    
    post_serializer = PostSerializer(post)
    
    page.posts.add(post)
    page.posts_count = page.posts_count + 1
    
    page.save()
    
    # notification = create_notification(request, 'page_post', page_id=page.id)
    
    serializer = PageSerializer(page)

    return JsonResponse({
        'page': serializer.data,
        'post': post_serializer.data,
    }, safe=False)

@api_view(['POST'])
def page_story_create(request, page_id):
    form = StoryForm(request.POST)
    if form.is_valid():
        story = form.save(commit=False)
        story.created_by = request.user
        story.save()

        attachments = request.FILES.getlist('image')
        videos = request.FILES.getlist('video')

        for attachment in attachments:
            attachment_instance = PostAttachment.objects.create(image=attachment, created_by=request.user)
            story.attachments.add(attachment_instance)

        for video in videos:
            video_instance = PostVideo.objects.create(video=video, created_by=request.user)
            story.videos.add(video_instance)
            
        story_serializer = StorySerializer(story)

        page = Page.objects.get(id=page_id)
    
        page.stories.add(story)        
        page.save()
        
        serializer = PageSerializer(page)

        return JsonResponse({
        'page': serializer.data,
        'story': story_serializer.data,
    }, safe=False)

@api_view(['POST'])
def page_post_like(request, page_id, post_id):
    page = Page.objects.get(id=page_id)    
    post = page.posts.get(id=post_id)
    
    if post.likes.filter(created_by=request.user).exists():
        like = post.likes.get(created_by=request.user)
        post.likes.remove(like)
        post.likes_count = post.likes_count - 1
        post.save()
        return JsonResponse({'message': 'post already liked'})
    
    like = Like.objects.create(created_by=request.user)
    post.likes.add(like)
    post.likes_count = post.likes_count + 1
    post.save()
    
    # notification = create_notification(request, 'post_like', post_id=post.id)
    
    return JsonResponse({'message': 'page like created'})


@api_view(['POST'])
def page_post_create_comment(request, page_id, post_id):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)
    
    page = Page.objects.get(id=page_id) 
    post = page.posts.get(id=post_id)
    
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()
    
    # notification = create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)

@api_view(['DELETE'])
def page_post_delete(request, page_id, post_id):
    page = Page.objects.get(id=page_id)    
    post = page.posts.filter(created_by=request.user).get(id=post_id)
    post.delete()

    return JsonResponse({'message': 'post deleted'})