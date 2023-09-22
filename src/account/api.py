import jwt
import datetime
from django.conf import settings
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import exceptions
from rest_framework.response import Response

from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer
from .forms import ProfileForm
from .authenticate import generate_access_token
from notification.utils import create_notification

@api_view(['POST'])
def signup_view(request, *args, **kwargs):
    data = request.data
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException("Password Does not match")
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return Response(serializer.data)

@api_view(['POST'])
def editprofile(request):
    user = request.user
    email = request.data.get('email')
    # firstname = request.data.get('firstname')
    # lastname = request.data.get('lastname')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return Response({'message': 'email already exists'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
        
        serializer = UserSerializer(user)

        return Response({'message': 'information updated', 'user': serializer.data})

@api_view(['POST'])
def login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return Response({'Message': 'You are already logged in ...'}, status=400)
    email = request.data.get("email")
    password = request.data.get("password")
    
    user = ( 
            User.objects.filter(Q(email__iexact=email) | Q(password__iexact=password))
            .distinct()
            .first()
    )
    
    if user is None:
        raise exceptions.AuthenticationFailed("user not found")

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("Incorrect password")

    response = Response()
    token = generate_access_token(user)
    response.set_cookie(key="jwt", value=token, httponly=True, expires=datetime.datetime.utcnow() + datetime.timedelta(days=30))
    response.data = {"jwt": token}
    return response


@api_view(["POST"])
def logout_view(request):
    response = Response()
    response.delete_cookie(key="jwt")
    response.data = {"message": "success logout"}
    return response

@api_view(["GET"])
def user_detail(request):
    token = request.COOKIES.get('jwt')
    
    if not token:
        raise exceptions.AuthenticationFailed('Unauthenticated')
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Unauthenticated')
    
    user = User.objects.filter(id=payload['user_id']).first() 
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def friends(request, id):
    user = User.objects.get(id=id)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data

    friends = user.friends.all()

    return Response({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests
    })
    
@api_view(['POST'])
def send_friendship_request(request, id):
    user = User.objects.get(id=id)

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)
    
    if not check1 and not check2:
        friendrequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        
        notification = create_notification(request, 'new_friendrequest', friendrequest_id=friendrequest.id)
        
        return Response({'message': 'friendship request created'})
    else:
        return Response({'message': 'request already sent'})


@api_view(['POST'])
def handle_request(request, id, status):
    user = User.objects.get(id=id)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    if friendship_request.status == FriendshipRequest.ACCEPTED:
    
        user.friends.add(request.user)
        user.friends_count = user.friends_count + 1
        user.save()

        request_user = request.user
        request_user.friends.add(user)
        request_user.friends_count = request_user.friends_count + 1
        request_user.save()
        
        notification = create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)

    return Response({'message': 'friendship request updated'})

@api_view(['POST'])
def unfollow(request, id):
    try:
        user = User.objects.get(id=id)
        request_user = request.user
        
        if request_user.friends.filter(id=user.id).exists():
            user.friends.remove(request_user)
            user.friends_count -= 1
            user.save()
            
            request_user.friends.remove(user)
            request_user.friends_count -= 1
            request_user.save()
            
            return Response({'message': 'Friendship deleted.'})
        else:
            return Response({'message': 'You are not friends with this user.'})
    except User.DoesNotExist:
        return Response({'message': 'User not found.'})