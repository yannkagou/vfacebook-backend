from rest_framework import serializers

from .models import User, FriendshipRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'firstname', 'lastname', 'birthday', 'tel', 'password', 'friends_count', 'posts_count', 'get_avatar',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'created_by', 'created_at_formatted',)