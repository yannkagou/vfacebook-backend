from django.db import models
from account.models import User
from post.models import Post

class Notification(models.Model):
    NEWFRIENDREQUEST = 'new_friendrequest'
    ACCEPTEDFRIENDREQUEST = 'accepted_friendrequest'
    REJECTEDFRIENDREQUEST = 'rejected_friendrequest'
    POST_LIKE = 'post_like'
    POST_COMMENT = 'post_comment'
    
    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEWFRIENDREQUEST, 'New friendrequuest'),
        (ACCEPTEDFRIENDREQUEST, 'Accepted friendrequest'),
        (REJECTEDFRIENDREQUEST, 'Rejected friendrequest'),
        (POST_LIKE, 'Post like'),
        (POST_COMMENT, 'Post comment'),
    )
    
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



# from django.db import models
# from account.models import User
# from page.models import Page
# from post.models import Post

# class Notification(models.Model):
#     NEWFRIENDREQUEST = 'new_friendrequest'
#     ACCEPTEDFRIENDREQUEST = 'accepted_friendrequest'
#     REJECTEDFRIENDREQUEST = 'rejected_friendrequest'
#     POST_LIKE = 'post_like'
#     POST_COMMENT = 'post_comment'
#     PAGE_LIKED = 'page_liked'
#     PAGE_POST = 'page_post'
#     PAGE_ADMIN = 'page_admin'
    
#     CHOICES_TYPE_OF_NOTIFICATION = (
#         (NEWFRIENDREQUEST, 'New friendrequuest'),
#         (ACCEPTEDFRIENDREQUEST, 'Accepted friendrequest'),
#         (REJECTEDFRIENDREQUEST, 'Rejected friendrequest'),
#         (POST_LIKE, 'Post like'),
#         (POST_COMMENT, 'Post comment'),
#         (PAGE_LIKED, 'Page Liked'),
#         (PAGE_POST, 'Page Post'),
#         (PAGE_ADMIN, 'Page Admin'),
#     )
    
#     body = models.TextField()
#     is_read = models.BooleanField(default=False)
#     type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
#     page = models.ForeignKey(Page, on_delete=models.CASCADE, blank=True, null=True)
#     created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)
#     created_for = models.ManyToManyField(User, related_name='received_notifications')
#     created_at = models.DateTimeField(auto_now_add=True)
