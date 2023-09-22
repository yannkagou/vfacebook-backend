from rest_framework import serializers

from .models import Notification
from account.serializers import UserSerializer
from post.serializers import PostSerializer

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'body', 'is_read','type_of_notification', 'post_id', 'created_for_id')



# from rest_framework import serializers

# from .models import Notification
# from account.serializers import UserSerializer
# # from post.serializers import PostSerializer
# # from page.serializers import PageSerializer

# class NotificationSerializer(serializers.ModelSerializer):
#     created_for = UserSerializer(read_only=True, many=True)
#     class Meta:
#         model = Notification
#         fields = ('id', 'body', 'is_read', 'type_of_notification', 'post_id', 'page_id','created_for')