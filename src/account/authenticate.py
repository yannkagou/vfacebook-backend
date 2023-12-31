from django.contrib.auth import get_user_model
import jwt
import datetime
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

User = get_user_model()

def generate_access_token(user, *args, **kwargs):
    
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

class JWTauthentication(BaseAuthentication):
    
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")
        
        if not token:
            return None
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        
        user = User.objects.filter(id=payload["user_id"]).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed("User Not Found")
        return (user, None)