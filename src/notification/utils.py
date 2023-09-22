from .models import Notification
from post.models import Post
from account.models import FriendshipRequest

def create_notification(request, type_of_notification, post_id=None, friendrequest_id = None, created_for = None ):
    if type_of_notification == 'post_like':
        post = Post.objects.get(id=post_id)
        created_for = post.created_by
        body = f'{request.user.firstname} {request.user.lastname} liked one of your posts!'
    elif type_of_notification == 'post_comment':
        post = Post.objects.get(id=post_id)
        created_for = post.created_by
        body = f'{request.user.firstname} {request.user.lastname} commented on one of your posts!'
    elif type_of_notification == 'new_friendrequest':
        friendrequest = FriendshipRequest.objects.get(id=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.firstname} {request.user.lastname} sent you a friend request!'
    elif type_of_notification == 'accepted_friendrequest':
        body = f'{request.user.firstname} {request.user.lastname} accepted your friend request!'
    elif type_of_notification == 'rejected_friendrequest':
        body = f'{request.user.firstname} {request.user.lastname} rejected your friend request!'
        friendrequest = FriendshipRequest.objects.get(id=friendrequest_id)
        created_for = friendrequest.created_for
    
    notification = Notification.objects.create(
        body = body,
        type_of_notification = type_of_notification,
        post_id = post_id,
        created_by = request.user,
        created_for = created_for,
    )
    
    return notification





# from page.models import Page
# from .models import Notification
# from post.models import Post
# from account.models import FriendshipRequest

# def create_notification(request, type_of_notification, post_id=None, page_id=None, friendrequest_id=None):
#     if type_of_notification == 'post_like':
#         post = Post.objects.get(id=post_id)
#         created_for = post.created_by
#         body = f'{request.user.firstname} {request.user.lastname} liked one of your posts!'
        
#     elif type_of_notification == 'post_comment':
#         post = Post.objects.get(id=post_id)
#         created_for = post.created_by
#         body = f'{request.user.firstname} {request.user.lastname} commented on one of your posts!'
        
#     elif type_of_notification == 'page_liked':
#         page = Page.objects.get(id=page_id)
#         created_for = page.created_by
#         body = f'{request.user.firstname} {request.user.lastname} liked one of your pages!'
        
#     elif type_of_notification == 'page_post':
#         page = Page.objects.get(id=page_id)
#         created_for = page.subscribers.all()  # Assuming subscribers is a ManyToManyField in Page model
#         body = f'{page.name} added a post!'
        
#     elif type_of_notification == 'page_admin':
#         page = Page.objects.get(id=page_id)
#         created_for = page.admins.all()  # Assuming admins is a ManyToManyField in Page model
#         body = f'{page.name} added a new admin!'
        
#     elif type_of_notification == 'new_friendrequest':
#         friendrequest = FriendshipRequest.objects.get(id=friendrequest_id)
#         created_for = friendrequest.created_for
#         body = f'{request.user.firstname} {request.user.lastname} sent you a friend request!'
        
#     elif type_of_notification == 'accepted_friendrequest':
#         body = f'{request.user.firstname} {request.user.lastname} accepted your friend request!'
        
#     elif type_of_notification == 'rejected_friendrequest':
#         body = f'{request.user.firstname} {request.user.lastname} rejected your friend request!'
#         friendrequest = FriendshipRequest.objects.get(id=friendrequest_id)
#         created_for = friendrequest.created_for
    
#     notification = Notification.objects.create(
#         body=body,
#         type_of_notification=type_of_notification,
#         post_id=post_id,
#         created_by=request.user,
#     )
    
#     notification.created_for.set(created_for)  # Assign created_for to the ManyToManyField
    
#     return notification