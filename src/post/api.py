from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer

from .forms import PostForm, StoryForm
from .models import Post, Like, Comment, Trend, PostAttachment, PostVideo, Story
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer, StorySerializer, StoryDetailSerializer
from notification.utils import create_notification

@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    
    # trend = request.GET.get('trend', '')
    # if trend:
    #     posts = posts.filter(body__icontains='#' + trend)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, id):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    post = Post.objects.filter(Q(created_by_id__in=list(user_ids))).get(id=id)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['GET'])
def post_list_profile(request, id):   
    user = User.objects.get(id=id)
    posts = Post.objects.filter(created_by_id=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        attachments = request.FILES.getlist('image')
        videos = request.FILES.getlist('video')

        for attachment in attachments:
            attachment_instance = PostAttachment.objects.create(image=attachment, created_by=request.user)
            post.attachments.add(attachment_instance)

        for video in videos:
            video_instance = PostVideo.objects.create(video=video, created_by=request.user)
            post.videos.add(video_instance)

        request.user.posts_count += 1
        request.user.save()

        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid form data for post'})
    

@api_view(['POST'])
def post_like(request, id):
    post = Post.objects.get(id=id)
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
    
    if post.created_by != request.user:
        notification = create_notification(request, 'post_like', post_id=post.id)
        
    return JsonResponse({'message': 'like created'})


@api_view(['POST'])
def post_create_comment(request, id):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(id=id)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()
    
    notification = create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)

@api_view(['DELETE'])
def post_delete(request, id):
    post = Post.objects.filter(created_by=request.user).get(id=id)
    post.delete()
    
    request.user.posts_count -= 1
    request.user.save()

    return JsonResponse({'message': 'post deleted'})

@api_view
def get_trends(request):
    trends = Trend.objects.all()
    serializer = TrendSerializer(trends, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def story_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    stories = Story.objects.filter(created_by_id__in=list(user_ids))
    
    user_ids_with_stories = stories.values_list('created_by_id', flat=True)

    users_with_stories = User.objects.filter(id__in=user_ids_with_stories)

    users_serializer = UserSerializer(users_with_stories, many=True)
    
    stories_serializer = StorySerializer(stories, many=True)

    return JsonResponse({
        'users':  users_serializer.data,
        'stories': stories_serializer.data,
    }, safe=False)

def story_list_profile(request, id):  
    user = User.objects.get(id=id)
    stories = Story.objects.filter(created_by_id=id)

    stories_serializer = StorySerializer(stories, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'stories': stories_serializer.data,
        'user': user_serializer.data,
    }, safe=False)

@api_view(['GET'])
def story_detail(request, id):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    story = Story.objects.filter(Q(created_by_id__in=list(user_ids))).get(id=id)

    return JsonResponse({
        'story': StoryDetailSerializer(story).data
    })

@api_view(['DELETE'])
def story_delete(request, id):
    story = Story.objects.filter(created_by=request.user).get(id=id)
    story.delete()

    return JsonResponse({'message': 'story deleted'})

@api_view(['POST'])
def story_create(request):
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

        serializer = StorySerializer(story)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid form data for story'})