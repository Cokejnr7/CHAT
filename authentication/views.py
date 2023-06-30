import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,generics,exceptions
from .serializers import UserSerializer,LoginSerializer
from django.contrib.auth import get_user_model
from .token import generate_access_token,generate_refresh_token
# Create your views here.


User = get_user_model()

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email is None:
            raise exceptions.AuthenticationFailed("email must be provided")
        elif password is None:
            raise exceptions.AuthenticationFailed("password must be provided")
        
        user = User.objects.get(email=email).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed("no user with that email")
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")
        
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        
        serializer = UserSerializer(user)
        
        response = Response({"user":serializer.data,"token":access_token},status=status.HTTP_200_OK)
        
        response.set_cookie(key='refresh_token',value=refresh_token,httponly=True)
        
        return response
    
    
    
# def refresh_token():
        