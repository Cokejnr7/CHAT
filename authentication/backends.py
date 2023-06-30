import jwt
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class JWTAuthectication(authentication.BasicAuthentication):
    
    def authenticate(self, request):
        auth= authentication.get_authorization_header(request)
        
        if not auth:
            return
        
        prefix,token = auth.decode('utf-8').split(" ")
        
        try:
            payload = jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[settings.ALGORITHM,])
            user = User.objects.get(email=payload['email'])
            
            return (user,token)
            
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("invalid token")
        
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("token expired")